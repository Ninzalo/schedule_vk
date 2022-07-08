import json
import datetime
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from Lib.bot.getter import get_forms, get_facs, get_session_groups, get_groups, get_subgroups, closest_week
from config import data_folder


def stage_start_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('начать', color=VkKeyboardColor.PRIMARY)
    return keyboard


def stage_home_keyboard(subgroup: str):
    keyboard = VkKeyboard()
    if subgroup != "None":
        keyboard.add_button('Расписание выбранной группы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    keyboard.add_button('Расписание', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Другое', color=VkKeyboardColor.PRIMARY)
    return keyboard


def stage_other_keyboard(can_get_teachers: bool):
    keyboard = VkKeyboard()
    keyboard.add_button(f"Пароли", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    if can_get_teachers:
        keyboard.add_button(f"Преподаватели", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button("Рассылка расписания", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"🤖Информация о боте🤖", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"В начало", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_passwords_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Мои пароли', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_setting_passwords_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button(f"Открытая", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"Приватная", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_mail_keyboard(daily_mail: int, weekly_mail: int):
    keyboard = VkKeyboard()
    if daily_mail == 0:
        keyboard.add_button("Ежедневная рассылка", color=VkKeyboardColor.POSITIVE)
    else:
        keyboard.add_button("Ежедневная рассылка", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    if weekly_mail == 0:
        keyboard.add_button("Еженедельная рассылка", color=VkKeyboardColor.POSITIVE)
    else:
        keyboard.add_button("Еженедельная рассылка", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_form_keyboard():
    forms = get_forms()
    keyboard = VkKeyboard()
    for form in forms:
        keyboard.add_button(f"{form}", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button(f"Обновить формы", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"В начало", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_fac_keyboard(form: str):
    keyboard = VkKeyboard()
    facs = get_facs(form=form)
    for fac in facs[:8]:
        keyboard.add_button(f"{fac.strip()}", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button(f"К выбору формы обучения", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_group_keyboard(form: str, fac: str, group_page: int):
    keyboard = VkKeyboard()
    session_groups = get_session_groups(form=form, fac=fac)
    groups = get_groups(form=form, fac=fac)
    if len(session_groups) != 0:
        amount_of_groups = 3
        keyboard.add_button("Сессия", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    else:
        amount_of_groups = 4
    fin_num_group = group_page * amount_of_groups
    start_num_group = fin_num_group - amount_of_groups
    for group in groups[start_num_group:fin_num_group]:
        keyboard.add_button(f"{group.strip()}", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    if group_page != 1:
        if group_page != 2:
            keyboard.add_button(f"< Стр 1", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(f"< Стр {group_page - 1}", color=VkKeyboardColor.PRIMARY)
    if len(groups) - start_num_group > amount_of_groups:
        keyboard.add_button(f" Стр {group_page + 1} >", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"К выбору формы обучения", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_session_group_keyboard(form: str, fac: str, session_group_page: int):
    keyboard = VkKeyboard()
    groups = get_session_groups(form=form, fac=fac)
    amount_of_groups = 3
    keyboard.add_button("Обычное расписание", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    fin_num_group = session_group_page * amount_of_groups
    start_num_group = fin_num_group - amount_of_groups
    for group in groups[start_num_group:fin_num_group]:
        keyboard.add_button(f"{group.strip()}", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    if session_group_page != 1:
        if session_group_page != 2:
            keyboard.add_button(f"< Стр 1", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(f"< Стр {session_group_page - 1}", color=VkKeyboardColor.PRIMARY)
    if len(groups) - start_num_group > amount_of_groups:
        keyboard.add_button(f" Стр {session_group_page + 1} >", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"К выбору формы обучения", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_subgroup_keyboard(form: str, fac: str, group: str):
    keyboard = VkKeyboard()
    all_subgroups = get_subgroups(form=form, fac=fac, group=group)
    for item in range(1, all_subgroups + 1):
        keyboard.add_button(f"{str(item).strip()}", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button(f"К выбору группы", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_schedule_type_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button(f"Расписание по дням", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"Расписание на неделю", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"В начало", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(f"Подгруппы", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_date_keyboard(form: str, fac: str, group: str, date_page: int):
    keyboard = VkKeyboard()
    with open(f'{data_folder}\\{form}\\{fac}\\data\\schedule\\schedule_{group}.json') as f:
        data = json.load(f)
    fin_num_date = date_page * 4
    start_num_date = fin_num_date - 4
    new_data = []
    date_day = int(datetime.datetime.today().strftime("%d"))
    date_month = int(datetime.datetime.today().strftime("%m"))
    date_year = int(f'20{datetime.datetime.today().strftime("%y")}')
    for date in data:
        file_year = int(date['date'].split('-')[0])
        file_month = int(date['date'].split('-')[1])
        file_day = int(date['date'].split('-')[2])
        if file_year > date_year:
            new_data.append(date)
        elif file_year == date_year and file_month > date_month:
            new_data.append(date)
        elif file_year == date_year and file_month == date_month and file_day >= date_day:
            new_data.append(date)
    for date in new_data[start_num_date:fin_num_date]:
        keyboard.add_button(f"{date['lessons'][0]['day_of_week'].capitalize()} {date['date'].strip()}",
                            color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    buttons_in_row = 0
    if date_page != 1:
        if date_page != 2:
            keyboard.add_button(f"< Стр 1", color=VkKeyboardColor.PRIMARY)
            buttons_in_row += 1
        keyboard.add_button(f"< Стр {date_page - 1}", color=VkKeyboardColor.PRIMARY)
        buttons_in_row += 1
    if len(new_data[start_num_date + 4:fin_num_date + 4]) > 0:
        keyboard.add_button(f" Стр {date_page + 1} >", color=VkKeyboardColor.PRIMARY)
        buttons_in_row += 1
    if len(new_data[start_num_date + 4:fin_num_date + 4]) != 0 or buttons_in_row > 0:
        keyboard.add_line()
    keyboard.add_button(f"Обновить", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(f"В начало", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(f"Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_week_keyboard(week_page: int, form: str, fac: str, group: str, 
        subgroup: str, quality: int, mode: str):
    _, user_week_page = closest_week(form=form, fac=fac, group=group, 
            subgroup=subgroup, quality=quality, mode=mode)
    keyboard = VkKeyboard()
    if user_week_page != week_page - 1 and user_week_page != week_page and user_week_page != week_page + 1:
        if user_week_page != -1 and user_week_page != 0 and user_week_page != 1:
            keyboard.add_button(f"Ближайшая неделя", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
    keyboard.add_button(f"Текущая неделя", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    if week_page - 1 != 0:
        keyboard.add_button(f"< Стр {week_page - 1}", color=VkKeyboardColor.PRIMARY)
    if week_page + 1 != 0:
        keyboard.add_button(f"Стр {week_page + 1} >", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(f"Настройки", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(f"В начало", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(f"Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard


def stage_settings_week_keyboard(mode: str, quality: int):
    keyboard = VkKeyboard()
    if mode == 'night':
        keyboard.add_button(f"Светлый режим", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    else:
        keyboard.add_button(f"Темный режим", color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
    if quality == 1:
        keyboard.add_button(f"Высокое качество", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    else:
        keyboard.add_button(f"Низкое качество", color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
    keyboard.add_button(f"Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard
