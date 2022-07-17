import calendar
from typing import List, Tuple
from Lib.schedule.dates import parity_check
# from Lib.schedule.schedule_data import Schedule, Other


def schedule_create(teachers_data: List[dict]) -> List[dict]:
    all_dates = _get_all_dates(teachers_data=teachers_data)

    schedule = []
    for date in all_dates:
        for teacher_data in teachers_data:
            if date['parity'] in teacher_data['type_of_week']:
                dates = teacher_data['dates']
                for item in dates:
                    if item == date['date']:
                        day = int(date['date'].split('-')[2])
                        month = int(date['date'].split('-')[1])
                        year = int(date['date'].split('-')[0])
                        schedule.append({
                            'date': date["date"],
                            'all_subgroups': teacher_data['all_subgroups'],
                            'other': {
                                'num': teacher_data['num'],
                                'name': teacher_data['name'],
                                "subgroup": teacher_data['subgroup'],
                                "type_of_week": parity_check(day=day, 
                                    month=month, year=year),
                                "day_of_week": teacher_data['day_of_week'],
                                "lesson_name": teacher_data['lesson_name'],
                                "type_of_lesson": teacher_data['type_of_lesson'],
                                "room": teacher_data['room'],
                                'dates': teacher_data['dates']
                            }
                        })
    # print(len(schedule))

    schedule = _del_all_copies(schedule=schedule)

    schedule = _del_copies(new_schedule=schedule)

    schedule = _del_special_keys_copies(schedule=schedule)

    # print(len(new_schedule))
    schedule = _del_copies(new_schedule=schedule)

    schedule = _get_compact_variant(schedule=schedule)

    return schedule


def _get_min_and_max_year(teachers_data: List[dict]) -> Tuple[int, int]:
    all_dates = []
    for teacher_data in teachers_data:
        for file_data in teacher_data['dates']:
            all_dates.append(file_data)
    all_dates = set(all_dates)
    all_dates = list(all_dates)

    min_day_file = 10000
    min_month_file = 10000
    min_year_file = 10000

    max_day_file = 0
    max_month_file = 0
    max_year_file = 0

    for date in all_dates:
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])
        day = int(date.split('-')[2])
        if year < min_year_file:
            min_day_file = day
            min_month_file = month
            min_year_file = year
        elif year == min_year_file:
            if month <= min_month_file:
                if month == min_month_file:
                    if day <= min_day_file:
                        min_day_file = day
                        min_month_file = month
                        min_year_file = year
                else:
                    min_day_file = day
                    min_month_file = month
                    min_year_file = year

        if year > max_year_file:
            max_day_file = day
            max_month_file = month
            max_year_file = year
        elif year == max_year_file:
            if month >= max_month_file:
                if month == max_month_file:
                    if day >= max_day_file:
                        max_day_file = day
                        max_month_file = month
                        max_year_file = year
                else:
                    max_day_file = day
                    max_month_file = month
                    max_year_file = year

    return min_year_file, max_year_file


def _del_copies(new_schedule: List[dict]) -> List[dict]:
    new_schedule2 = []
    for old in [item for item in new_schedule]:
        copies = []
        for new in [entry for entry in new_schedule]:
            if old == new:
                copies.append(new)

        new_schedule2.append(copies[0])
        if len(copies) > 1:
            for copy in range(1, len(copies)):
                new_schedule.remove(copies[copy])
    return new_schedule2


def _del_all_copies(schedule: List[dict]) -> List[dict]:
    new_schedule = []
    for old in schedule:
        if old['other']['subgroup'] == '':
            is_ok2 = True
            for new in schedule:
                if new['other']['subgroup'] != '':
                    list_of_equals = ['name', 'day_of_week', 'num', 
                            'lesson_name', 'type_of_lesson', 'room']
                    is_ok = True
                    for equal in list_of_equals:
                        if old['date'] == new['date']:
                            if old['other'][equal] != new['other'][equal]:
                                is_ok = False
                        else:
                            is_ok = False
                    if is_ok:
                        is_ok2 = False
                        new_schedule.append(new)
            if is_ok2:
                new_schedule.append(old)
        else:
            new_schedule.append(old)
    return new_schedule


def _del_special_keys_copies(schedule: List[dict]) -> List[dict]:
    new_schedule = []
    for item in [item for item in schedule]:
        copies = []
        for entry in schedule:
            if (item['date'] == entry['date'] and 
                item['other']['num'] == entry['other']['num'] and 
                item['other']['subgroup'] == entry['other']['subgroup']
                ):
                copies.append(entry)
        min_len_of_dates = 1000
        min_index = 0
        for entry in enumerate(copies):
            if len(entry[1]['other']['dates']) <= min_len_of_dates:
                min_len_of_dates = len(entry[1]['other']['dates'])
                min_index = entry[0]

        if len(copies) > 1:
            for copy in enumerate(copies):
                if copy[0] != min_index:
                    schedule.remove(copy[1])
        new_schedule.append(copies[min_index])
    return new_schedule


def _get_compact_variant(schedule: List[dict]) -> List[dict]:
    new_schedule = []
    for item in schedule:
        new_schedule.append({
            'date': item['date'],
            'all_subgroups': item['all_subgroups'],
            "other": {
                'num': item['other']['num'],
                'name': item['other']['name'],
                'subgroup': item['other']['subgroup'],
                'type_of_week': item['other']['type_of_week'],
                'day_of_week': item['other']['day_of_week'],
                'lesson_name': item['other']['lesson_name'],
                'type_of_lesson': item['other']['type_of_lesson'],
                'room': item['other']['room'],
                # "dates": item['other']['dates']
            }
        })
    return new_schedule


def _get_all_dates(teachers_data: List[dict]) -> List[dict]:
    min_year_file, max_year_file = _get_min_and_max_year(
            teachers_data=teachers_data)

    all_dates = []
    for year in range(min_year_file, max_year_file + 1):
        for month in range(1, 13):
            for day in range(1, calendar._monthlen(year, month) + 1):
                all_dates.append({
                    'date': f'{year}-{month}-{day}',
                    'parity': parity_check(day=day, month=month, year=year)
                })
    return all_dates


def compress(data: List[dict]) -> List[dict]:
    days = []
    for old in [item for item in data]:
        day = {
            'date': old['date'],
            'all_subgroups': old['all_subgroups'],
        }
        lessons = []
        for new in data:
            if new['date'] == day['date']:
                lessons.append(new['other'])
        temp = []
        for x in lessons:
            if x not in temp:
                temp.append(x)
        lessons = temp
        day['lessons'] = lessons
        days.append(day)

    days2 = [item for item in days]
    days = []
    for old in days2:
        if old['date'] not in [item['date'] for item in days]:
            days.append(old)
    del days2
    return days
