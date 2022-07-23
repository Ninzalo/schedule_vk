import datetime
import time
from Lib.bot.BotDB_Func import BotDB_Func
from config import group_id, db_path, bot_start_time, bot_close_time

db = BotDB_Func(db_path=db_path)

def group_online(vk_session):
    online = vk_session.method('groups.getOnlineStatus', {'group_id': group_id}) 
    time_now = int(datetime.datetime.now().strftime('%H'))
    if online['status'] == 'none':
        if time_now >= bot_start_time or time_now < bot_close_time:
            enable_online = vk_session.method('groups.enableOnline', 
                    {'group_id': group_id}) 
            if enable_online != 1:
                return print(f'Failed to turn on online')
    elif online['status'] == 'online':
        if time_now >= bot_close_time and time_now < bot_start_time:
            disable_online = vk_session.method('groups.disableOnline', 
                    {'group_id': group_id}) 
            if disable_online != 1:
                return print(f'Failed to turn off online')


def wall_sender(post: str, sender):
    users = db.get_users()
    text = 'Обновление!'
    for user_id in users:
        try:
            sender(id=user_id, text=text, preuploaded_doc=post)
            time.sleep(0.3)
        except:
            pass
