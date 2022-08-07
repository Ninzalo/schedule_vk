from typing import List, Tuple, Type
from Lib.schedule.find import find_cell
from Lib.schedule.cell_data import Cell
from Lib.schedule.dates import only, since

def get_num_of_lesson(book: List[Cell], cell: Cell) -> Cell:
    """ Gets num of lesson """
    num_of_lesson = find_cell(
            book=book, 
            sheet=cell.sheet, 
            row=cell.row - 1, 
            col=cell.col - 4)

    if num_of_lesson.value == '':
        iteration = 0
        while True:
            num_of_lesson = find_cell(
                    book=book, 
                    sheet=cell.sheet, 
                    row=cell.row - iteration, 
                    col=cell.col - 4)
            if num_of_lesson.value != '':
                break
            iteration += 1
    return num_of_lesson

def get_type_of_week(book: List[Cell], cell: Cell) -> Cell:
    """ Gets type of week """
    type_of_week = find_cell(
            book=book, 
            sheet=cell.sheet, 
            row=cell.row - 1, 
            col=cell.col - 3)
    if type_of_week.value == '' and find_cell(
            book=book, sheet=cell.sheet, 
            row=cell.row-1, 
            col=cell.col-2).top_line_style != 'thin':
        iteration = 0
        while find_cell(book=book, sheet=cell.sheet, 
                row=cell.row-iteration, 
                col=cell.col-2).top_line_style != 'thin':
            iteration += 1
            type_of_week =find_cell(
            book=book, sheet=cell.sheet, 
            row=cell.row-iteration, 
            col=cell.col-3)
    if type_of_week.value == '':
        type_of_week.value = 'ВН'

    return type_of_week


def get_type_of_lesson(book: List[Cell], cell: Cell) -> Cell:
    """ Gets type of lesson """
    type_of_lesson = find_cell(
            book=book, 
            sheet=cell.sheet, 
            row=cell.row, 
            col=cell.col - 2)
    return type_of_lesson


def get_name_of_lesson(book: List[Cell], cell: Cell) -> Cell:
    """ Gets name of lesson """
    lesson_name = find_cell(
            book=book, 
            sheet=cell.sheet, 
            row=cell.row - 1, 
            col=cell.col - 2)

    if lesson_name.top_line_style != 'thin' and lesson_name.top_line_style != 'dashDot':
        iteration = 0
        while True:
            if find_cell(book=book, sheet=cell.sheet, 
                    row=cell.row - iteration, 
                    col=cell.col - 2
                    ).top_line_style == 'thin' and find_cell(
                    book=book, sheet=cell.sheet, 
                    row=cell.row - iteration - 1, 
                    col=cell.col - 2
                    ).bottom_line_style == 'no_line':
                lesson_name = find_cell(
                                book=book, 
                                sheet=cell.sheet, 
                                row=cell.row - iteration, 
                                col=cell.col - 2)
                break
            if find_cell(book=book, sheet=cell.sheet, 
                    row=cell.row - iteration, 
                    col=cell.col - 2
                    ).top_line_style == 'dashDot' and find_cell(
                    book=book, sheet=cell.sheet, 
                    row=cell.row - iteration - 1, 
                    col=cell.col - 2
                    ).bottom_line_style == 'no_line':
                lesson_name = find_cell(
                                book=book, 
                                sheet=cell.sheet, 
                                row=cell.row - iteration, 
                                col=cell.col - 2)
                break
            iteration += 1
        print('Изменение имени', lesson_name.value)

    return lesson_name


def get_room(book: List[Cell], cell: Cell) -> Cell:
    room = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row, 
                col=cell.col + 2)
    return room


def get_day_of_week(book: List[Cell], cell: Cell) -> Cell:
    """ Gets day of week """
    days_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 
                    'суббота', 'воскресенье']
    iteration = 0

    while True:
        is_ok = False

        day_of_week = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row - iteration, 
                col=cell.col)

        day_of_week_name = ""
        for letter in day_of_week.value:
            if letter != " ":
                day_of_week_name += f'{letter}'
        day_of_week.value = day_of_week_name.lower()

        for item in days_of_week:
            if day_of_week.value == item:
                is_ok = True
        if is_ok:
            break
        iteration += 1

    return day_of_week


def get_dates(book: List[Cell], cell: Cell) -> Cell:
    dates = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row + 1, 
                col=cell.col - 2)
    iteration = 0
    if dates.value == '':
        while True:
            dates_cell = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row + iteration, 
                col=cell.col - 2)

            if dates_cell.bottom_line_style == 'thin':
                dates = dates_cell
                break
            if dates_cell.bottom_line_style == 'dashDot':
                dates = dates_cell
                break
            iteration += 1

    if '.' not in dates.value:
        iteration = 0
        while True:
            dates_cell = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row - iteration, 
                col=cell.col - 2)

            if dates_cell.top_line_style == 'thin' or dates_cell.top_line_style == 'dashDot':
                if '.' in str(dates_cell.value).strip():
                    if ', т' in str(dates_cell.value).strip():
                        dates = dates_cell
                        dates.value = f'т{str(dates.value).strip().split(", т")[1]}'
                    if ', с' in str(dates_cell.value).strip():
                        dates = dates_cell
                        dates.value = f'с{str(dates.value).strip().split(", с")[1]}'
                break

            iteration += 1

    if '.' not in dates.value:
        dates_value = str(cell.value).split(',')
        if len(dates_value) > 2:
            for item in dates_value:
                if 'только' in item or ' с ' in dates_value:
                    if '.' in item:
                        dates.value = item.strip()

    if '.' not in dates.value:
        iteration = 0
        while True:
            dates_cell = find_cell(
                book=book, 
                sheet=cell.sheet, 
                row=cell.row - iteration, 
                col=cell.col - 2)

            if dates_cell.top_line_style == 'thin':
                if ', ' in dates_cell.value:
                    dates_value2 = str(dates_cell.value).split(', ')
                    for item in dates_value2:
                        if 'только' in item or ' с ' in item:
                            dates.value = item.strip()
                break
            iteration += 1

    # if type(dates.value) == list:
        # if '.' not in dates.value:
            # try:
                # for date in dates.value:
            # except:
                # pass
    
    return dates


def get_dates_list(book: List[Cell], dates: Cell, day_of_week: Cell, 
        type_of_week: Cell) -> Cell:
    if "только" in dates.value:
        dates.value = only(dates_value=dates.value,
                           book=book)

    if 'с' in dates.value:
        dates.value = since(dates_value=dates.value,
                            day_of_week_value=day_of_week.value,
                            type_of_week_value=type_of_week.value,
                            book=book)
    return dates



def get_subgroup(cell: Cell) -> str:
    """ gets subgroup """
    if cell.sheet != 0:
        subgroup = str(cell.sheet - 1)
    else:
        subgroup = ''
    return subgroup
