import calendar
import datetime
import xlrd
from typing import List
from Lib.schedule.cell_data import Cell
from Lib.schedule.find import find_cell
from Lib.schedule.getter import get_num_of_lesson, get_type_of_week, get_type_of_lesson, get_name_of_lesson, get_room, get_day_of_week, get_dates, get_dates_list, get_subgroup
# from Lib.schedule.dates import only, since


def styles_fetch(style: int) -> str:
    if style == 0:
        ret_style = 'no_line'
    elif style == 1:
        ret_style = 'thin'
    elif style == 9:
        ret_style = 'dashDot'
    else: 
        ret_style = 'no_line'
    return ret_style


def book_to_list(path) -> list:
    workbook = xlrd.open_workbook(path, formatting_info=True)
    worksheet_names = workbook.sheet_names()

    book_data = []
    # for worksheet_name in worksheet_names:
    for worksheet_name in reversed(range(0, len(worksheet_names))):
        # worksheet = workbook.sheet_by_name(worksheet_name)
        worksheet = workbook.sheet_by_index(worksheet_name)
        # row_data = []
        for row in range(0, worksheet.nrows):
            # cell_data = []
            for col in range(0, worksheet.ncols):
                cell = worksheet.cell_value(row, col)
                line_style = worksheet.cell(row, col).xf_index
                line_style = workbook.xf_list[line_style]
                top_line_style = styles_fetch(line_style.border.top_line_style)
                bottom_line_style = styles_fetch(line_style.border.bottom_line_style)
                if type(cell) == str:
                    pass
                else:
                    if cell > worksheet.nrows:
                        dt = xlrd.xldate_as_tuple(cell, workbook.datemode) 
                        cell = str(datetime.datetime(*dt).strftime("%Y-%m-%d"))
                    else:
                        cell = str(int(cell))
                cell = cell.strip()

                cell_data = Cell(value=cell, row=row, col=col, 
                            sheet=worksheet_name, 
                            top_line_style=top_line_style, 
                            bottom_line_style=bottom_line_style)
                book_data.append(cell_data)
                # print(f'{abc(j=col)}{row+1} row_num - {row} | '\
                        # f'col_num - {col} | sheet_name - {worksheet_name} '\
                        # f'| {cell}' )
                # cell_data.append((row, col, cell))
            # row_data.append((row, cell_data))
        # book_data.append((worksheet_name, row_data))
    return book_data


def find_max_sheet(book: List[Cell]) -> int:
    max_sheet = 0
    for cell in book:
        if cell.sheet > max_sheet:
            max_sheet = cell.sheet
    return max_sheet + 1


def get_teachers_data(book_data: List[Cell]):
    teachers_data = []
    for cell in book_data:
        if cell.sheet != 1:
            if cell.col == 4:
                if cell.value != '':
                    if '.' in cell.value and ',' in cell.value:
                        name = cell.value

                        """ Gets num of lesson """
                        num_of_lesson = get_num_of_lesson(book=book_data, 
                                                    cell=cell)

                        """ Gets type of week """
                        type_of_week = get_type_of_week(book=book_data, 
                                                    cell=cell)

                        """ Gets type of lesson """
                        type_of_lesson = get_type_of_lesson(book=book_data, 
                                                        cell=cell)

                        """ Gets name of lesson """
                        lesson_name = get_name_of_lesson(book=book_data, 
                                                    cell=cell)

                        """ Gets room """
                        room = get_room(book=book_data, cell=cell)

                        """ Gets day of week """
                        day_of_week = get_day_of_week(book=book_data, cell=cell)

                        """ Gets dates """
                        dates = get_dates(book=book_data, cell=cell)

                        if '.' in dates.value:
                            """ Gets dates list """
                            dates = get_dates_list(book=book_data, 
                                    dates=dates, day_of_week=day_of_week, 
                                    type_of_week=type_of_week)

                            """ gets subgroup """
                            subgroup = get_subgroup(cell=cell)

                            """ json adding """
                            list_of_equals = ['name', 'day_of_week', 
                                    'type_of_week', 'num', 'lesson_name',
                                    'type_of_lesson', 'room', 'dates']

                            is_ok = True
                            data = {
                                'name': str(name).split(",")[0].strip(),
                                'all_subgroups': find_max_sheet(book=book_data) - 2,
                                "day_of_week": str(day_of_week.value).strip(),
                                "subgroup": subgroup.strip(),
                                "type_of_week": str(type_of_week.value).strip(),
                                'num': str(num_of_lesson.value).strip(),
                                "lesson_name": str(lesson_name.value).strip(),
                                "type_of_lesson": str(type_of_lesson.value).strip(),
                                "room": str(room.value).strip(),
                                "dates": dates.value
                            }
                            if data['subgroup'] == "":
                                for teacher_data in teachers_data:
                                    if teacher_data['subgroup'] != '':
                                        is_ok2 = True
                                        for equal in list_of_equals:
                                            if teacher_data[equal] != data[equal]:
                                                is_ok2 = False
                                        if is_ok2:
                                            is_ok = False
                            del_data = []
                            if data['subgroup'] != "":
                                for teacher_data in teachers_data:
                                    if teacher_data['subgroup'] == '':
                                        is_ok2 = True
                                        for equal in list_of_equals:
                                            if teacher_data[equal] != data[equal]:
                                                is_ok2 = False
                                        if is_ok2:
                                            del_data.append(teacher_data)

                            for item in del_data:
                                teachers_data.remove(item)
                            if is_ok:
                                teachers_data.append(data)
                        else:
                            print(f'В ячейче с датами нет "." - {dates.value} '\
                                f'\n| Ячейка с типом предмета - '\
                                f'{str(type_of_lesson.value).strip()} '\
                                f'\n| Ячейка с названием предмета - '\
                                f'{str(lesson_name.value).strip()} '\
                                f'\n| Ячейка с именем препода - '\
                                f'{str(name).strip()}')
    return teachers_data

def abc(j):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet[j]

def xlrd_test(path: str):
    workbook = xlrd.open_workbook(path)
    worksheet_names = workbook.sheet_names()
    for worksheet_name in worksheet_names:
        worksheet = workbook.sheet_by_name(worksheet_name)
        for i in range(0, worksheet.nrows):
            for j in range(0, worksheet.ncols):
                cell = worksheet.cell_value(i, j)
                if type(cell) == str:
                    pass
                else:
                    cell = str(int(cell))
                # if cell != '':
                print(f'{abc(j=j)}{i+1} row_num - {i} | col_num - {j} | sheet_name - {worksheet_name} | {cell}' )

