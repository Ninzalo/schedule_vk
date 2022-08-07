import os
import time
from datetime import datetime
from typing import List


def _deleter(path: str) -> None:
    try:
        os.remove(path)
    except:
        pass

def delete_old_files(files: List[str], start_day: int, start_hour: int, 
                    start_minute: int) -> None:
    for file in files:
        # last_change = str(time.ctime(os.path.getmtime(file))).strip().split(' ')
        # print(last_change)
        # last_change = [i for i in last_change]
        last_edit_time = time.ctime(os.path.getmtime(file))
        last_edit_datetime = datetime.strptime(
                last_edit_time, 
                '%a %b %d %H:%M:%S %Y')
        last_edit_day = last_edit_datetime.strftime('%d')
        last_edit_hour = last_edit_datetime.strftime('%H')
        last_edit_minute = last_edit_datetime.strftime('%M')
        change_day = int(last_edit_day)
        change_hour = int(last_edit_hour)
        change_minute = int(last_edit_minute)

        # change_day = int(last_change[2])
        # change_hour = int(last_change[3].split(':')[0])
        # change_minute = int(last_change[3].split(':')[1])
        if start_day != change_day:
            _deleter(path=file)
            print(f'Удален старый файл, измененный {last_edit_datetime} - {file}')
        else:
            if change_hour < start_hour:
                _deleter(path=file)
                print(f'Удален старый файл, '\
                    f'измененный {last_edit_datetime} - {file}')
            elif change_hour == start_hour and change_minute < start_minute:
                _deleter(path=file)
                print(f'Удален старый файл, '\
                    f'измененный {last_edit_datetime} - {file}')


def del_all_files_in_folders(folders: List[str]) -> None:
    for folder in folders:
        for item in os.listdir(folder):
            try:
                os.remove(f'{folder}\\{item}')
            except:
                pass

def remove_empty_folders(path: str) -> None:
    while True:
        all_files = []
        for dirs, folders, files, in os.walk(path):
            if len(folders) == 0 and len(files) == 0:
                os.rmdir(dirs)
                all_files.append(dirs)
                print(len(folders), len(files), dirs)
        print(len(all_files))
        if len(all_files) == 0:
            break
