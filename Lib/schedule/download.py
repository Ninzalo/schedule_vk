import requests
import os
import time
import random
import urllib3
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys

from config import data_folder, mstuca_url


def download() -> None:
    urllib3.disable_warnings()
    all_amount_of_files = 0
    ua = UserAgent()
    session = requests.Session()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    url = f"{mstuca_url}/students/shedule/"
    r = retry(session=session, headers=headers, url=url)
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", class_="news-list")
    url_to_fac = soup.find_all('a')

    urls = []
    for url in url_to_fac:
        if 'students' in url.get('href'):
            if "все направления" not in url.find('b').text.strip().lower() and 'зачетно-экз' not in url.find('b').text.strip().lower():
                urls.append(f"{mstuca_url}/{url.get('href')}")

    time.sleep(2)

    for url in urls[:]:
        r = retry(session=session, headers=headers, url=url)

        data = []
        soup = BeautifulSoup(r.text, "lxml")
        names_of_fac = soup.find('div', class_="breadcrumb")
        name_of_fac = names_of_fac.find_all('li')[6]
        form = names_of_fac.find_all('li')[8]
        name_of_fac = name_of_fac.find('span').text.strip()
        form = form.find('span').text.strip()

        try:
            name_of_fac = name_of_fac.split('(')[1].split(')')[0]
        except:
            pass

        print(name_of_fac, form)

        soup = soup.find("div", class_="news-list")
        all_news = soup.find_all("p", class_="news-item")
        for news in all_news:
            names = news.find("b").text.strip().split(" ")

            names = [item.strip() for item in names]
            name = ''
            for item in names:
                try: 
                    int(item.split('.')[0])
                except:
                    if item != '':
                        name += f' {item}'

            if name != '':
                try:
                    link = f'{mstuca_url}{news.find("a").get("href")}'
                    data.append({
                        "link": link,
                        "name": name
                    })
                except:
                    print(f'[ ERROR ] Ошибка в {names}')
            else:
                print(f'[ ERROR ] Ошибка в {names}')

        if not os.path.exists(f"{data_folder}\\{form}"):
            os.mkdir(f"{data_folder}\\{form}")

        if not os.path.exists(f"{data_folder}\\{form}\\{name_of_fac}"):
            os.mkdir(f"{data_folder}\\{form}\\{name_of_fac}")

        if not os.path.exists(f"{data_folder}\\{form}\\{name_of_fac}\\xls"):
            os.mkdir(f"{data_folder}\\{form}\\{name_of_fac}\\xls")

        if not os.path.exists(f"{data_folder}\\{form}\\{name_of_fac}\\data"):
            os.mkdir(f"{data_folder}\\{form}\\{name_of_fac}\\data")

        iter = 1
        for item in data:
            try:
                get_file = retry(session=session, headers=headers, 
                        url=item['link'], stream=True)
                xls_path = f"{data_folder}\\{form}\\{name_of_fac}\\xls"\
                        f"\\{item['name'].strip()}.xls"
                with open(xls_path, "wb") as file:
                    for chunk in get_file.iter_content(chunk_size=576 * 1024):
                        if chunk:
                            file.write(chunk)
                print(f'[INFO] Downloaded {" " if iter < 10 else ""}'\
                    f'{iter} / {len(data)} book ( {item["name"].strip()} )')
                iter += 1
                all_amount_of_files += 1
                time.sleep(2)
            except Exception as ex:
                print(ex)
    print(f'[INFO] All amoount of files: {all_amount_of_files}')


def retry(session, headers: dict, url: str, 
        stream: bool|None = None) -> requests.models.Response:
    retries = 0
    while True:
        if stream is not None:
            r = session.get(url=url, headers=headers, stream=stream, 
                    verify=False)
        else:
            r = session.get(url=url, headers=headers, verify=False)
        if '[200' in str(r):
            return r
        retries += 1
        time.sleep(random.randrange(1, 5))
        if retries >= 50:
            print(f'[INFO] Сайт лег!')
            sys.exit(0)
