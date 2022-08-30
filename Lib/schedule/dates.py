from Lib.schedule.cell_data import Cell
from typing import List, Literal, Union
import datetime
import calendar


def only(dates_value, book: List[Cell]) -> List[str]:
    dates_value = dates_value.split(' ')[1]
    if ";" in dates_value:
        dates_value = dates_value.split(';')

    if type(dates_value) != list:
        dates_value = [dates_value]

    """ gets year """

    dates = []
    for date_value in dates_value:
        date_to_compare = date_value.split('.')
        day_to_compare = date_to_compare[0]
        month_to_compare = date_to_compare[1]
        md_to_compare = f'-{month_to_compare}-{day_to_compare}'
        for item in book:
            if md_to_compare in item.value:
                year = str(item.value).split('-')[0]
                dates.append(f'{int(year)}-{int(month_to_compare)}-{int(day_to_compare)}')

    return dates


def since(dates_value, day_of_week_value: str|List[str], 
        type_of_week_value: str|List[str], book: List[Cell]) -> List[str]:

    minuses_list = []
    if 'кроме' in dates_value:
        minuses = dates_value.split('кроме')[1].strip()
        if ';' in minuses:
            minuses = minuses.split(";")
        if type(minuses) != list:
            minuses = [minuses]
        for minus in minuses:
            date_to_compare = minus.split('.')
            day_to_compare = date_to_compare[0]
            month_to_compare = date_to_compare[1]
            md_to_compare = f'-{month_to_compare}-{day_to_compare}'
            for item in book:
                if md_to_compare in item.value:
                    year: Union[int, str] = str(item.value).split('-')[0]
                    minuses_list.append(f'{int(year)}-{int(month_to_compare)}-{int(day_to_compare)}')

    """ gets since date """
    since_date = dates_value.split('по')[0].split('с')[1].strip()
    since_day = since_date.split('.')[0]
    since_day_int = int(since_day)
    since_month = since_date.split('.')[1]
    since_month_int = int(since_month)

    """ gets until date """
    until_date = dates_value.split('по')[1].strip()
    if 'кроме' in until_date:
        until_date = until_date.split('кроме')[0].strip()
    until_day = until_date.split('.')[0]
    until_day_int = int(until_day)
    until_month = until_date.split('.')[1]
    until_month_int = int(until_month)

    """ gets since year """
    since_year = ''
    md_to_compare = f'-{since_month}-{since_day}'
    for item in book:
        if md_to_compare in item.value:
            since_year = str(item.value).split('-')[0]
    if since_year == '':
        since_year = datetime.datetime.today().strftime("%Y")
    since_year_int = int(since_year)

    """ gets until year """
    until_year = ''
    md_to_compare = f'-{until_month}-{until_day}'
    for item in book:
        if md_to_compare in item.value:
            until_year = str(item.value).split('-')[0]
    if until_year == '':
        until_year = since_year
    until_year_int = int(until_year)

    dates = []

    if since_month_int > until_month_int:
        for year in range(since_year_int, until_year_int+1):
            if year == since_year_int:
                for month in range(since_month_int, 13):
                    if month == since_month_int:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = since_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        max_day_in_month = calendar._monthlen(year, month)
                        for day in range(since_day_int, 
                            max_day_in_month + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day,
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    if (day <= until_day_int and 
                                        month <= until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')
                                    elif (day > until_day_int and 
                                        month != until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')

                    elif month == until_month_int:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = until_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        for day in range(1, until_day_int + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day, 
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    if (day <= until_day_int and 
                                        month <= until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')
                                    elif (day > until_day_int and 
                                        month != until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')

                    else:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = since_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        max_day_in_month = calendar._monthlen(year, month)
                        for day in range(1, max_day_in_month + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day, 
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    dates.append(f'{year}-{month}-{day}')
            if year == until_year_int:
                for month in range(1, until_month_int):
                    if month == since_month_int:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = since_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        max_day_in_month = calendar._monthlen(year, month)
                        for day in range(since_day_int, 
                            max_day_in_month + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day, 
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    if (day <= until_day_int and 
                                        month <= until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')
                                    elif (day > until_day_int and 
                                        month != until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')

                    elif month == until_month_int:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = until_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        for day in range(1, until_day_int + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day, 
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    if (day <= until_day_int and 
                                        month <= until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')
                                    elif (day > until_day_int and 
                                        month != until_month_int):
                                        dates.append(f'{year}-{month}-'\
                                            f'{day}')

                    else:
                        if len(str(month)) < 2:
                            md_to_compare = f'-0{month}-'
                        else:
                            md_to_compare = f'-{month}-'
                        year = since_year
                        for item in book:
                            if md_to_compare in item.value:
                                year = str(item.value).split('-')[0]
                        year = int(year)
                        max_day_in_month = calendar._monthlen(year, month)
                        for day in range(1, max_day_in_month + 1):
                            if calendar_fetch(month=month, day=day, 
                                year=year) == day_of_week_value:
                                date_type_of_week = parity_check(day=day, 
                                    month=month, year=year)
                                if date_type_of_week in type_of_week_value:
                                    dates.append(f'{year}-{month}-{day}')
    else:
        for month in range(since_month_int, until_month_int + 1):
            if month == since_month_int:
                if len(str(month)) < 2:
                    md_to_compare = f'-0{month}-'
                else:
                    md_to_compare = f'-{month}-'
                year = since_year
                for item in book:
                    if md_to_compare in item.value:
                        year = str(item.value).split('-')[0]
                year = int(year)
                max_day_in_month = calendar._monthlen(year, month)
                for day in range(since_day_int, max_day_in_month + 1):
                    if calendar_fetch(month=month, day=day, year=year) == day_of_week_value:
                        date_type_of_week = parity_check(day=day, month=month, year=year)
                        if date_type_of_week in type_of_week_value:
                            if day <= until_day_int and month <= until_month_int:
                                dates.append(f'{year}-{month}-{day}')
                            elif day > until_day_int and month != until_month_int:
                                dates.append(f'{year}-{month}-{day}')

            elif month == until_month_int:
                if len(str(month)) < 2:
                    md_to_compare = f'-0{month}-'
                else:
                    md_to_compare = f'-{month}-'
                year = until_year
                for item in book:
                    if md_to_compare in item.value:
                        year = str(item.value).split('-')[0]
                year = int(year)
                for day in range(1, until_day_int + 1):
                    if calendar_fetch(month=month, day=day, year=year) == day_of_week_value:
                        date_type_of_week = parity_check(day=day, month=month, year=year)
                        if date_type_of_week in type_of_week_value:
                            if day <= until_day_int and month <= until_month_int:
                                dates.append(f'{year}-{month}-{day}')
                            elif day > until_day_int and month != until_month_int:
                                dates.append(f'{year}-{month}-{day}')

            else:
                if len(str(month)) < 2:
                    md_to_compare = f'-0{month}-'
                else:
                    md_to_compare = f'-{month}-'
                year = since_year
                for item in book:
                    if md_to_compare in item.value:
                        year = str(item.value).split('-')[0]
                year = int(year)
                max_day_in_month = calendar._monthlen(year, month)
                for day in range(1, max_day_in_month + 1):
                    if calendar_fetch(month=month, day=day, year=year) == day_of_week_value:
                        date_type_of_week = parity_check(day=day, month=month,  year=year)
                        if date_type_of_week in type_of_week_value:
                            dates.append(f'{year}-{month}-{day}')

    if len(minuses_list) != 0:
        for item in minuses_list:
            try:
                dates.remove(item)
            except:
                pass

    # print(dates)
    return dates


def calendar_fetch(month, day, year):
    current_weekday = calendar.day_abbr[
        datetime.date(
            year=year,
            month=month,
            day=day
        ).weekday()
    ]
    if current_weekday == "Mon":
        current_weekday = "понедельник"
    elif current_weekday == "Tue":
        current_weekday = "вторник"
    elif current_weekday == "Wed":
        current_weekday = "среда"
    elif current_weekday == "Thu":
        current_weekday = "четверг"
    elif current_weekday == "Fri":
        current_weekday = "пятница"
    elif current_weekday == "Sat":
        current_weekday = "суббота"
    else:
        current_weekday = "воскресенье"
    return current_weekday


def parity_check(day: int, month: int, year: int) -> Literal['Н', 'В']:
    now = datetime.datetime.now().replace(year=year, month=month, day=day)

    sep = datetime.datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)

    d1 = sep - datetime.timedelta(days=sep.weekday())
    d2 = now - datetime.timedelta(days=now.weekday())

    parity = ((d2 - d1).days // 7) % 2
    # print(f"{datetime.datetime.today().strftime('%Y')}-{month}-{day} parity: {'Нижняя' if parity else 'Верхняя'}")
    if parity:
        date_type_of_week = "Н"
    else:
        date_type_of_week = 'В'

    return date_type_of_week
