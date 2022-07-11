import requests
import os
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from config import data_folder 


def download():
    all_amount_of_files = 0
    ua = UserAgent()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Cookie": "BITRIX_SM_GUEST_ID=7910540; BX_USER_ID=2686dd73b2c2dcfad961a83e1d6c674f; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A3%2C%22EXPIRE%22%3A1655931540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; PHPSESSID=bOIhX2c1Yjllvv4cSzI44l3tpOYLEZ8X; BITRIX_SM_LAST_VISIT=22.06.2022+11%3A02%3A44",
        "Connection": "keep-alive",
        'User-Agent': ua.random,
    }

    url = "http://mstuca.ru/students/shedule/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", class_="news-list")
    url_to_fac = soup.find_all('a')

    urls = []
    for url in url_to_fac:
        if 'students' in url.get('href'):
            if "все направления" not in url.find('b').text.strip().lower() and 'зачетно-экз' not in url.find('b').text.strip().lower():
                urls.append(f"http://mstuca.ru/{url.get('href')}")

    time.sleep(2)

    for url in urls[:]:
        r = requests.get(url=url, headers=headers)

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
                    link = f'http://mstuca.ru{news.find("a").get("href")}'
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

        if not os.path.exists(f"{data_folder}\\{form}\\{name_of_fac}\\xlsx"):
            os.mkdir(f"{data_folder}\\{form}\\{name_of_fac}\\xlsx")

        if not os.path.exists(f"{data_folder}\\{form}\\{name_of_fac}\\data"):
            os.mkdir(f"{data_folder}\\{form}\\{name_of_fac}\\data")

        iter = 1
        for item in data:
            try:
                get_file = requests.get(item['link'], stream=True)
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
