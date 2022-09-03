import os
import time
from datetime import datetime
from typing import List


def _deleter(path: str) -> None:
    try:
        os.remove(path)
    except:
        pass

def delete_old_files(files: List[str], start_time: datetime) -> None:
    for file in files:
        last_edit_time = time.ctime(os.path.getmtime(file))
        last_edit_datetime = datetime.strptime(
            last_edit_time, 
            '%a %b %d %H:%M:%S %Y')
        if last_edit_datetime < start_time:
            _deleter(path=file)
            print(f'Удален старый файл, измененный '\
                f'{last_edit_datetime} - {file}')


def del_all_files_in_folders(folders: List[str]) -> None:
    for folder in folders:
        for item in os.listdir(folder):
            try:
                os.remove(f'{folder}/{item}')
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
