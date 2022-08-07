import os
from typing import Literal, List
from Lib.schedule.cell_data import Cell


Allowed_exts = Literal['.xls', '.xlsx', '.json', '.jpg']

def find_file_with_ext(location: str, ext_to_find: Allowed_exts|List[Allowed_exts], 
        ext_to_miss: Allowed_exts|None|List[Allowed_exts] = None) -> List[str]:

    all_files = []
    for dirs, _, files, in os.walk(location):
        for file in files:
            """ Если тип расширения - str """
            if type(ext_to_find) == str: 
                if ext_to_find in str(os.path.join(dirs, file)):
                    if ext_to_miss is not None:
                        """ Если тип расширения - str """
                        if type(ext_to_miss) == str:
                            if ext_to_miss not in str(os.path.join(dirs, file)):
                                all_files.append(str(os.path.join(dirs, file)))

                            """ Если тип расширения - list """
                        elif type(ext_to_miss) == list:
                            is_ok = True
                            for miss_item in ext_to_miss:
                                if miss_item in str(os.path.join(dirs, file)):
                                    is_ok = False
                            if is_ok:
                                all_files.append(str(os.path.join(dirs, file)))
                    else:
                        all_files.append(str(os.path.join(dirs, file)))

                """ Если тип расширения - list """
            elif type(ext_to_find) == list:
                for find_item in ext_to_find:
                    if find_item in str(os.path.join(dirs, file)):
                        if ext_to_miss is not None:
                            """ Если тип расширения - str """
                            if type(ext_to_miss) == str:
                                if ext_to_miss not in str(os.path.join(dirs, file)):
                                    all_files.append(str(os.path.join(dirs, file)))

                                """ Если тип расширения - list """
                            elif type(ext_to_miss) == list:
                                is_ok = True
                                for miss_item in ext_to_miss:
                                    if miss_item in str(os.path.join(dirs, file)):
                                        is_ok = False
                                if is_ok:
                                    all_files.append(str(os.path.join(dirs, file)))
                        else:
                            all_files.append(str(os.path.join(dirs, file)))

    return all_files


def find_folder_with_name(location: str, folder_name: str) -> List[str]:
    output_folders = []
    for dirs, folders, _, in os.walk(location):
        for folder in folders:
            if folder_name in str(os.path.join(dirs, folder)):
                output_folders.append(str(os.path.join(dirs, folder)))
    return output_folders


def create_empty_folders(folders: list) -> None:
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)


def find_cell(book: List[Cell], sheet: int, row: int, col: int) -> Cell:
    for cell in book:
        if cell.sheet == sheet and cell.row == row and cell.col == col:
            return cell
    return Cell(value='', row=0, col=0, sheet=0, top_line_style='no_line', 
            bottom_line_style='no_line')


