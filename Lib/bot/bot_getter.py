import os
import requests
import json
import datetime
from typing import List, Tuple, Optional, Union, Type, Any
from vk_api.keyboard import VkKeyboard
from Lib.bot.event_hint import Event_hint
from Lib.bot.BotDB_Func import BotDB_Func
from config import data_folder, db_path

db = BotDB_Func(db_path=db_path)

def get_forms() -> List[str]:
    forms = []
    for _, folders, _, in os.walk(data_folder):
        forms.append(folders)
    forms[0].sort()
    return forms[0]


def get_facs(form: str) -> List[str]:
    form_folder = get_form_path(form=form)
    facs = []
    for _, folders, _, in os.walk(form_folder):
        facs.append(folders)
    facs[0].sort()
    return facs[0]


def get_groups(form: str, fac: str) -> List[str]:
    schedule_data_folder = get_schedule_folder_path(form=form, fac=fac)
    list_of_groups = os.listdir(schedule_data_folder)
    groups = []
    for item in list_of_groups:
        if '.json' in item and 'сесс' not in item:
            groups.append(item.split('.json')[0].split("schedule_")[1])
    groups.sort()
    return groups


def get_session_groups(form: str, fac: str) -> List[str]:
    schedule_data_folder = get_schedule_folder_path(form=form, fac=fac)
    list_of_groups = os.listdir(schedule_data_folder)
    groups = []
    for item in list_of_groups:
        if '.json' in item and 'сесс' in item:
            groups.append(item.split('.json')[0].split("schedule_")[1])
    groups.sort()
    return groups


def get_subgroups(form: str, fac: str, group: str) -> int:
    path = get_schedule_path(form=form, fac=fac, group=group)
    with open(path) as f:
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
    days = [(today_date - datetime.timedelta(days=delta)).strftime('%Y-%m-%d') 
            for delta in reversed(range(0, today_num + 1))]
    days += ([(today_date + datetime.timedelta(days=delta)).strftime('%Y-%m-%d') 
            for delta in range(1, 7 - today_num)])
    dates = []
    for date in days:
        date_split: List[str] = date.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])
        date = f'{year}-{month}-{day}'
        dates.append(date)
    
    first_date_str: str = dates[0]
    last_date_str: str = dates[-1]
    return first_date_str, last_date_str


def closest_week(form: str, fac: str, group: str, subgroup: str, 
        quality: int, mode: str) -> Tuple[Tuple[Any, str], int]:
    change = 0
    while True:
        user_week_page = change
        first_date, last_date = week_dates_gen(user_week_page=user_week_page)
        error = week_check(form=form, fac=fac, group=group, subgroup=subgroup, 
                quality=quality, mode=mode, first_date=first_date, 
                last_date=last_date)
        if error == 0:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        user_week_page = -change
        first_date, last_date = week_dates_gen(user_week_page=user_week_page)
        error = week_check(form=form, fac=fac, group=group, subgroup=subgroup, 
                quality=quality, mode=mode, first_date=first_date, 
                last_date=last_date)
        if error == 0:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        if change >= 300:
            closest_week_dates = first_date, last_date
            return closest_week_dates, user_week_page
        change += 1


def week_check(form: str, fac: str, group: str, subgroup: str, quality: int, 
        mode: str, first_date: str, last_date: str) -> int:
    doc = get_schedule_picture_path(form=form, fac=fac, group=group, 
        subgroup=subgroup, quality=quality, mode=mode, 
        first_date=first_date, last_date=last_date)
    if os.path.exists(doc):
        error = 0
    else:
        error = 1
    return error


def week_schedule(vk, form: str, fac: str, group: str, subgroup: str, 
        quality: int, mode: str, user_id: int, first_date: str, 
        last_date: str, event=None) -> Tuple[str, int]:
    try:
        doc = get_schedule_picture_path(form=form, fac=fac, group=group, 
            subgroup=subgroup, quality=quality, mode=mode, 
            first_date=first_date, last_date=last_date)
        if event is not None:
            doc = doc_uploader(vk=vk, doc=doc, event=event, 
                    first_date=first_date, last_date=last_date)
        else:
            doc = doc_uploader(vk=vk, doc=doc, peer_id=user_id, 
                    first_date=first_date, last_date=last_date)
        error = 0
        return doc, error
    except:
        doc = ''
        error = 1
        return doc, error

def doc_uploader(vk, doc, first_date: str, last_date: str, 
        peer_id: int | None=None, event=None) -> str:
    if event is not None:
        result = json.loads(requests.post(
            vk.docs.getMessagesUploadServer(type='doc', 
                peer_id=event.peer_id)['upload_url'],
            files={'file': open(doc, 'rb')}).text)
    else:
        result = json.loads(requests.post(
            vk.docs.getMessagesUploadServer(type='doc', 
                peer_id=peer_id)['upload_url'],
            files={'file': open(doc, 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], 
            title=f'{first_date}-{last_date}', tags=[])
    document = f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
    return document

def get_first_and_last_date(type_of_week: str, form: str, 
        fac: str, group: str, subgroup: str, quality: int, 
        mode: str, user_id:int) -> Tuple[str, str, int]:
    """ Получаем first_date, last_date и user_week_page"""
    if type_of_week == 'closest':
        closest_week_dates, user_week_page = closest_week(
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


def get_all_weeks(vk, id: int, event: Event_hint, 
        type_of_week: str, stage_week_keyboard) -> Tuple[str, str, VkKeyboard]:
    """ type_of_week = 'closest' | 'now' | 'next' | 'prev' """

    """ Получаем данные пользователя """
    form = db.get_form(user_id=id)
    fac = db.get_fac(user_id=id)
    group = db.get_group(user_id=id)
    subgroup = db.get_subgroup(user_id=id)
    quality = db.get_quality(user_id=id)
    mode = db.get_mode(user_id=id)

    """ Получаем first_date, last_date и user_week_page """
    first_date, last_date, user_week_page = get_first_and_last_date(
            type_of_week=type_of_week, 
            form=form, 
            fac=fac, 
            group=group, 
            subgroup=subgroup, 
            quality=quality, 
            mode=mode, 
            user_id=id
            )

    """ Меняем week_page пользователя """
    db.change_week_page(user_id=id, week_page=user_week_page)

    """ Получаем файл расписания и код ошибки """
    doc, error = week_schedule(
            vk=vk, 
            form=form, 
            fac=fac, 
            group=group, 
            subgroup=subgroup, 
            quality=quality, 
            mode=mode, 
            user_id=id, 
            first_date=first_date, 
            last_date=last_date, 
            event=event
            )

    """ Получаем выводимый текст """
    if error == 0:
        text = f'Неделя {first_date} - {last_date}'
        if type_of_week == 'closest':
            text += ' (Ближайшая)'
        elif type_of_week == 'now':
            text += ' (Текущая)'
    else:
        text = f'Нет расписания на {first_date} - {last_date}'

    """ Получаем stage7_keyboard """
    keyboard = stage_week_keyboard(
            week_page=user_week_page, 
            form=form, 
            fac=fac, 
            group=group, 
            subgroup=subgroup, 
            quality=quality, 
            mode=mode
            )
    return text, doc, keyboard


def get_form_path(form: str) -> str:
    form_folder = f'{data_folder}\\{form}'
    return form_folder


def get_fac_path(form: str, fac: str) -> str:
    form_folder = get_form_path(form=form)
    fac_folder = f'{form_folder}\\{fac}'
    return fac_folder


def get_schedule_folder_path(form: str, fac: str) -> str:
    fac_folder = get_fac_path(form=form, fac=fac)
    schedule_folder_path = f'{fac_folder}\\data\\json\\schedule'
    return schedule_folder_path


def get_week_folder_path(form: str, fac: str) -> str:
    fac_folder = get_fac_path(form=form, fac=fac)
    week_folder_path = f'{fac_folder}\\data\\week'
    return week_folder_path 


def get_schedule_path(form: str, fac: str, group: str) -> str:
    schedule_path = get_schedule_folder_path(form=form, fac=fac)
    path = f'{schedule_path}\\schedule_{group}.json'
    return path


def get_schedule_picture_path(form: str, fac: str, group: str, 
        subgroup: str, quality: int, mode: str, first_date: str, 
        last_date: str) -> str:
    week_path = get_week_folder_path(form=form, fac=fac)
    path = f'{week_path}\\{group}\\s{subgroup}\\q{quality}\\{mode}'\
            f'\\week_{first_date}_{last_date}.jpg'
    return path
