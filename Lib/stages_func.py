from Lib.getter import week_schedule, get_first_and_last_date
from Lib.keyboards import *
from Lib.event_hint import Event_hint
from typing import Tuple
from vk_api.keyboard import VkKeyboard


def get_all_weeks(data_folder:str, vk, db, id: int, event: Event_hint, 
        type_of_week: str) -> Tuple[str, str, VkKeyboard]:
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
            data_folder=data_folder, 
            type_of_week=type_of_week, 
            form=form, 
            fac=fac, 
            group=group, 
            subgroup=subgroup, 
            quality=quality, 
            mode=mode, 
            db=db,
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
            data_folder=data_folder, 
            week_page=user_week_page, 
            form=form, 
            fac=fac, 
            group=group, 
            subgroup=subgroup, 
            quality=quality, 
            mode=mode
            )
    return text, doc, keyboard
