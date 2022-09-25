import os
import datetime
import json
from typing import List, NamedTuple
from Lib.bot.output_texts import error_teachers_str 
from Lib.bot.BotDB_Func import Teacher_search
from config import data_folder

ts = Teacher_search()

class Teacher(NamedTuple):
    teacher_name: str
    lessons: List[List[str]]
    lessons_pages: int

class Search_result(NamedTuple):
    result_str: str
    data: List[Teacher]

class Search_fetch(NamedTuple):
    result_str: str
    max_teachers: int
    max_pages: int


def search_fetch(teacher_page: int, data_page: int, name: str
    ) -> Search_fetch:
    search_result = _find_teacher(name=name)
    return_str = search_result.result_str
    try:
        if teacher_page > len(search_result.data)-1:
            needed_teacher = search_result.data[len(search_result.data)-1]
        else:
            needed_teacher = search_result.data[teacher_page]
        return_str += needed_teacher.teacher_name
        if data_page > needed_teacher.lessons_pages-1:
            for lesson in needed_teacher.lessons[
                needed_teacher.lessons_pages-1]:
                return_str += lesson
        else:
            for lesson in needed_teacher.lessons[data_page]:
                return_str += lesson
        max_pages=needed_teacher.lessons_pages-1
        max_teachers=len(search_result.data)-1
    except:
        return_str = error_teachers_str(name=name)
        max_pages = 0
        max_teachers = 0
    return Search_fetch(result_str=return_str, 
        max_pages=max_pages,
        max_teachers=max_teachers)


def _find_teacher(name: str) -> Search_result:
    teachers_data = _get_teacher_data()
    result = []
    for teacher_item in teachers_data:
        if name.lower() in str(teacher_item.get('name')).lower():
            result.append(teacher_item)
    fetched_data = _fetch_data(data=result)
    search_result = _return_string(data=fetched_data, name=name)
    return search_result 


def full_search_string(name: str) -> str:
    teachers_data = _get_teacher_data()
    result = []
    for teacher_item in teachers_data:
        if name.lower() in str(teacher_item.get('name')).lower():
            result.append(teacher_item)
    fetched_data = _fetch_data(data=result)
    string = _full_search_fetch(name=name, data=fetched_data)
    return string


def _full_search_fetch(name: str, data: List[dict]) -> str:
    string = _return_full_string(data=data, name=name)
    if len(string) > 4090:
        for days_limit in [120, 90, 60, 50, 40, 30, 20, 10, 7]:
            if len(string) > 4090:
                string = _return_full_string(data=data, 
                    name=name, max_days=days_limit)
            else: 
                break
        if len(string) > 4090:
            string = error_teachers_str(name=name)
    return string


def _return_full_string(name: str, data: List[dict], 
    max_days: None|int = None) -> str:
    result = f'Результаты поиска "{name}"'
    if max_days:
        result += f'\nПоказаны результаты на ближайшие {max_days} дней'
    now = datetime.datetime.today()
    now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    for teacher in data:
        result += f'\n\n\nИмя: {teacher.get("name")}'
        checkpoint = str(result)
        for date in teacher['dates']:
            date_datetime = datetime.datetime.strptime(
                date['date'],'%Y-%m-%d')
            if date_datetime >= now:
                if max_days:
                    if (date_datetime - now).days <= max_days:
                        result += f'\n\nДата: {date.get("date")}'
                        result += f'\nАудитория: {date.get("room")}'
                        result += f'\nПара: {date.get("num")}'
                        result += f'\nПредмет: {date.get("lesson_name")}'
                else:
                    result += f'\n\nДата: {date.get("date")}'
                    result += f'\nАудитория: {date.get("room")}'
                    result += f'\nПара: {date.get("num")}'
                    result += f'\nПредмет: {date.get("lesson_name")}'
        if result == checkpoint:
            result += f'\n\nУ преподавателя больше нет пар :с'
    return result


def _get_teacher_data() -> List[dict]:
    result = []
    for dirs, _, files in os.walk(data_folder):
        for file in files:
            if 'teachers_' in str(file):
                teacher_data = _get_file_data(
                        path=dirs, 
                        filename=file
                    )
                for teacher in teacher_data:
                    result.append(teacher)
    return result


def _get_file_data(path: str, filename: str) -> List[dict]:
    with open(f'{path}/{filename}', encoding='utf-8') as teacher_data_raw:
        teacher_data = json.load(teacher_data_raw)
    return teacher_data


def _fetch_data(data: List[dict]) -> List[dict]:
    all_names = _get_all_names(data=data)
    info_per_name = _get_info_per_name(data=data, names=all_names)
    info_per_name = _get_info_per_lesson_name(data=data, 
        info_per_name=info_per_name)
    return info_per_name 


def _get_info_per_lesson_name(data: List[dict], 
    info_per_name: List[dict]) -> List[dict]:
    result = []
    for teacher in info_per_name:
        struct = {
                    'name': teacher.get('name'),
                    'dates': []
                 }
        dates = []
        for lesson_name in teacher['lessons_names']:
            for data_item in data:
                if (
                    data_item.get('name') == teacher.get('name') and
                    data_item.get('lesson_name') == lesson_name
                    ):
                    for date in data_item['dates']:
                        if date not in dates:
                            dates.append(
                                    {
                                        'date': date,
                                        'room': data_item.get('room'),
                                        'num': data_item.get('num'),
                                        "lesson_name": data_item.get(
                                            'lesson_name')
                                    }
                                )
        dates = _dates_sort(dates)
        for date in dates:
            struct['dates'].append(date)
        result.append(struct)
    return result


def _dates_sort(dates: List[dict]) -> List[dict]:
    dates.sort(key=lambda date: 
            (
                datetime.datetime.strptime(date['date'], '%Y-%m-%d'),
                date.get('num')
            )
        )
    dates = _remove_date_copies(dates=dates)
    return dates 


def _remove_date_copies(dates: List[dict]) -> List[dict]:
    result = []
    for date in dates:
        if not date in result:
            result.append(date)
    return result


def _remove_list_copies(data: list) -> list:
    result = []
    for item in data:
        if not item in result:
            result.append(item)
    return result


def _get_info_per_name(data: List[dict], names: List[str]) -> List[dict]:
    result = []
    for name in names:
        name_dict = {
                        'name': name,
                        'lessons_names': [],
                    }
        for data_item in data:
            if data_item.get('name') == name:
                if not data_item.get(
                    'lesson_name') in name_dict[
                    'lessons_names']:
                    name_dict['lessons_names'].append(
                        data_item.get('lesson_name'))
        result.append(name_dict)
    return result


def _get_all_names(data: List[dict]) -> List[str]:
    result = []
    for names in data:
        if not names.get('name') in result:
            result.append(names.get('name'))
    return result


def _return_string(name: str, data: List[dict]) -> Search_result:
    result_str = f'Результаты поиска "{name}"'
    now = datetime.datetime.today()
    now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    teachers_list = []
    for teacher in data:
        teacher_name = f'\n\n\nИмя: {teacher.get("name")}'
        lessons_list = []
        lessons_items_list = []
        start_datetime = now
        last_adding = []
        for date in teacher['dates']:
            date_datetime = datetime.datetime.strptime(
                date['date'],'%Y-%m-%d')
            result = ''
            if date_datetime >= now:
                result += f'\n\nДата: {date.get("date")}'
                result += f'\nАудитория: {date.get("room")}'
                result += f'\nПара: {date.get("num")}'
                result += f'\nПредмет: {date.get("lesson_name")}'
                if result != '':
                    if date_datetime >= (start_datetime + 
                        datetime.timedelta(days=1)):
                        if len(lessons_items_list) != 0:
                            if lessons_items_list not in lessons_list:
                                lessons_list.append(lessons_items_list)
                        if len(lessons_items_list) > 4:
                            lessons_items_list = []
                        lessons_items_list.append(result)
                        start_datetime = date_datetime
                    else:
                        lessons_items_list.append(result)
                        last_adding = lessons_items_list
        if lessons_list == []:
            result = f'\n\nУ преподавателя больше нет пар :с'
            lessons_items_list.append(result)
            last_adding = lessons_items_list
        if last_adding not in lessons_list:
            lessons_list.append(last_adding)
        lessons_list = _remove_list_copies(data=lessons_list)
        teacher_data = Teacher(teacher_name=teacher_name,
            lessons=lessons_list, lessons_pages=len(lessons_list))
        teachers_list.append(teacher_data)
    return Search_result(result_str=result_str, data=teachers_list)
