import os
import requests
import json
import datetime
from typing import List, Tuple
from Lib.event_hint import Event_hint


def get_forms(data_folder: str) -> List[str]:
    forms = []
    for _dirs, folders, _files, in os.walk(data_folder):
        forms.append(folders)
    return forms[0]


def get_facs(data_folder: str, form: str) -> List[str]:
    data_folder = f'{data_folder}\\{form}'
    facs = []
    for _dirs, folders, _files, in os.walk(data_folder):
        facs.append(folders)
    return facs[0]


def get_groups(data_folder: str, form: str, fac: str) -> List[str]:
    data_folder = f"{data_folder}\\{form}\\{fac}\\data\\schedule"
    list_of_groups = os.listdir(data_folder)
    groups = []
    for item in list_of_groups:
        if '.json' in item and 'сесс' not in item:
            groups.append(item.split('.json')[0].split("schedule_")[1])
    return groups


def get_session_groups(data_folder: str, form: str, fac: str) -> List[str]:
    data_folder = f"{data_folder}\\{form}\\{fac}\\data\\schedule"
    list_of_groups = os.listdir(data_folder)
    groups = []
    for item in list_of_groups:
        if '.json' in item and 'сесс' in item:
            groups.append(item.split('.json')[0].split("schedule_")[1])
    return groups


def get_subgroups(data_folder: str, form: str, fac: str, group: str) -> int:
    with open(f'{data_folder}\\{form}\\{fac}\\data\\schedule\\schedule_{group}.json') as f:
        data = json.load(f)
    all_subgroups = 0
    for item in data[:3]:
        all_subgroups = item['all_subgroups']
    return all_subgroups


def week_dates_gen(user_week_page: int) -> Tuple[str, str]:
    delta = user_week_page
    first_date = datetime.datetime.today()
    today_date = first_date + datetime.timedelta(days=delta*7)
    today_date = today_date.strftime('%Y-%m-%d') 
    today_date = datetime.datetime.strptime(today_date, '%Y-%m-%d')
    today_num = today_date.weekday()
    days = [(today_date - datetime.timedelta(days=delta)).strftime('%Y-%m-%d') for delta in reversed(range(0, today_num + 1))]
    days += ([(today_date + datetime.timedelta(days=delta)).strftime('%Y-%m-%d') for delta in range(1, 7 - today_num)])
    dates = []
    for date in days:
        date = date.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        date = f'{year}-{month}-{day}'
        dates.append(date)
    
    first_date = dates[0]
    last_date = dates[-1]
    return first_date, last_date


def closest_week(data_folder: str, form: str, fac: str, group: str, subgroup: str, quality: int, mode: str):
    change = 0
    while True:
        user_week_page = change
        first_date, last_date = week_dates_gen(user_week_page=user_week_page)
        error = week_check(data_folder=data_folder, form=form, fac=fac, group=group, subgroup=subgroup, quality=quality, mode=mode, first_date=first_date, last_date=last_date)
        if error == 0:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        user_week_page = -change
        first_date, last_date = week_dates_gen(user_week_page=user_week_page)
        error = week_check(data_folder=data_folder, form=form, fac=fac, group=group, subgroup=subgroup, quality=quality, mode=mode, first_date=first_date, last_date=last_date)
        if error == 0:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        if change >= 300:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        change += 1


def week_check(data_folder: str, form: str, fac: str, group: str, subgroup: str, quality: int, mode: str, first_date, last_date) -> int:
    doc = f'{data_folder}\\{form}\\{fac}\\data\\schedule\\{group}\\s{subgroup}\\q{quality}\\{mode}\\week_{first_date}_{last_date}.jpg'
    if os.path.exists(doc):
        error = 0
    else:
        error = 1
    return error


def week_schedule(vk, form: str, fac: str, group: str, subgroup: str, quality: int, mode: str, user_id: int, first_date: str, last_date: str, event=None):
    try:
        doc = f'{os.getcwd()}\\data\\{form}\\{fac}\\data\\schedule\\{group}\\s{subgroup}\\q{quality}\\{mode}\\week_{first_date}_{last_date}.jpg'
        if event is not None:
            doc = doc_uploader(vk=vk, doc=doc, event=event, first_date=first_date, last_date=last_date)
        else:
            doc = doc_uploader(vk=vk, doc=doc, peer_id=user_id, first_date=first_date, last_date=last_date)
        error = 0
        return doc, error
    except:
        doc = ''
        error = 1
        return doc, error

def doc_uploader(vk, doc, first_date:str, last_date: str, peer_id: int | None=None, event=None):
    if event is not None:
        result = json.loads(requests.post(
            vk.docs.getMessagesUploadServer(type='doc', peer_id=event.peer_id)['upload_url'],
            files={'file': open(doc, 'rb')}).text)
    else:
        result = json.loads(requests.post(
            vk.docs.getMessagesUploadServer(type='doc', peer_id=peer_id)['upload_url'],
            files={'file': open(doc, 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title=f'{first_date}-{last_date}', tags=[])
    document = f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
    return document

def get_first_and_last_date(data_folder: str, type_of_week: str, form: str, 
        fac: str, group: str, subgroup: str, quality: int, 
        mode: str, db, user_id:int) -> Tuple[str, str, int]:
    """ Получаем first_date, last_date и user_week_page"""
    if type_of_week == 'closest':
        closest_week_dates, user_week_page = closest_week(
                data_folder=data_folder, 
                form=form, 
                fac=fac, 
                group=group, 
                subgroup=subgroup, 
                quality=quality, 
                mode=mode
                )
        first_date, last_date = closest_week_dates
    else:
        if type_of_week == 'now':
            user_week_page = 0
        elif type_of_week == 'next':
            user_week_page = db.get_week_page(user_id=user_id)
            user_week_page += 1
        elif type_of_week == 'prev':
            user_week_page = db.get_week_page(user_id=user_id)
            user_week_page -= 1
        else:
            user_week_page = 0
        first_date, last_date = week_dates_gen(user_week_page=user_week_page)
    return first_date, last_date, user_week_page
