import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

if 'test' in str(Path(os.getcwd()).parent).lower().split(f'\\')[-1]:
    token_vk = str(os.getenv('TEST_API_KEY'))
    group_id = str(os.getenv('TEST_GROUP_ID'))
else:
    token_vk = str(os.getenv('MAIN_API_KEY'))
    group_id = str(os.getenv('MAIN_GROUP_ID'))


db_path = f'{os.getcwd()}\\Lib\\db\\schedule_vk.db'
data_folder = f'{os.getcwd()}\\data'
font_path = f'{os.getcwd()}\\Lib\\Fonts'
teachers_info_path = f'{os.getcwd()}\\Lib\\teachers_data'

mstuca_url = 'https://www.mstuca.ru'

delay = 55
time_str = '20.00'

bot_start_time = 5
bot_close_time = 1

show_elapsed_time = False
