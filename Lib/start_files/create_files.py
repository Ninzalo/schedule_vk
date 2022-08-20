import os
from pathlib import Path
from config import start_files_path

def bot_start_file(path: str) -> None:
    _create_folder()
    text = f'cd "{Path(path).parent}"\nvenv/Scripts/activate\n'\
            f'cd "{path}"\npython bot.py\npause'
    _create_file(text=text, filename='bot', ext='ps1')


def schedule_start_file(path: str) -> None:
    _create_folder()
    filename = 'schedule'
    text = f'cd "{Path(path).parent}"\nvenv/Scripts/activate\n'\
            f'cd "{path}"\npython schedule.py\npause'
    _create_file(text=text, filename=filename, ext='ps1')
    _schedule_bat_file(filename=filename)


def _schedule_bat_file(filename: str) -> None:
    text = f'start {start_files_path}/schedule.ps1'
    _create_file(text=text, filename=filename, ext='bat')


def _create_folder() -> None:
    if not os.path.exists(start_files_path):
        os.mkdir(start_files_path)


def _create_file(text: str, filename: str, ext: str) -> None:
    if not os.path.exists(f'{start_files_path}/{filename}.{ext}'):
        with open(f'{start_files_path}/{filename}.{ext}', 'w') as f:
            f.write(text)
