import os
import time
from typing import List

def _deleter(path: str):
    try:
        os.remove(path)
    except:
        pass

def delete_old_files(files: List[str], start_day: int, start_hour: int, 
                    start_minute: int):
    for file in files:
        last_change = str(str(time.ctime(os.path.getmtime(file))).strip().split(' '))
        last_change = [i for i in last_change if i != '']
        change_day = int(last_change[2])
        change_hour = int(last_change[3].split(':')[0])
        change_minute = int(last_change[3].split(':')[1])
        if start_day != change_day:
            _deleter(path=file)
            print(f'Удален старый файл, измененный {last_change} - {file}')
        else:
            if change_hour < start_hour:
                _deleter(path=file)
                print(f'Удален старый файл, '\
                    f'измененный {last_change} - {file}')
            elif change_hour == start_hour and change_minute < start_minute:
                _deleter(path=file)
                print(f'Удален старый файл, '\
                    f'измененный {last_change} - {file}')


def del_all_files_in_folders(folders: List[str]):
    for folder in folders:
        for item in os.listdir(folder):
            try:
                os.remove(f'{folder}\\{item}')
            except:
                pass

def remove_empty_folders(path: str):
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
