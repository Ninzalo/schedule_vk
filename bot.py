# -*- coding: utf-8 -*-

import time
import json
import vk_api
import datetime
import socket
import urllib3
import requests
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import token_vk, group_id, db_path, delay, time_str

from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.bot_func import Bot_class
from Lib.bot.sender import Sender
from Lib.bot.event_hint import Event_hint
from Lib.bot.stages_names import Stages_names

from Lib.bot.mail import daily_mail, weekly_mail

from Lib.bot.group import group_online, wall_sender
from Lib.bot.output_texts import passwords_info_str

from Lib.bot.table import create_tables

import multiprocessing


vk_session = vk_api.VkApi(token=token_vk)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

sender = Sender(vk_session=vk_session)
sn = Stages_names()
db = BotDB_Func(db_path=db_path)
bot_class = Bot_class(sender=sender, db=db, vk=vk)


def main():
    start_time = datetime.datetime.now()
    amount_of_old_messages = bot_class.old_messages(vk_session=vk_session)
    if amount_of_old_messages != 0:
        print(f'[INFO] {amount_of_old_messages} Old '\
            f'message{"s" if amount_of_old_messages > 1 else ""} '\
            f'answered in {datetime.datetime.now()-start_time}')
    del start_time, amount_of_old_messages

    print('[INFO] Bot started')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            event = Event_hint(
                    msg=event.object.message['text'].lower(),
                    message=event.object.message['text'], 
                    id=event.object.message['from_id'], 
                    peer_id=event.object.message['peer_id'],
                    button_actions=event.object.client_info['button_actions'], 
                    attachments=event.object.message['attachments']
                    )
            bot_class.bot(event=event)

            """ Обработка постов """
        elif event.type == VkBotEventType.WALL_POST_NEW:
            id_ = event.object['id']
            owner_id_ = event.group_id
            wall_id = f'wall-{owner_id_}_{id_}'
            wall_sender(post=wall_id, sender=sender.sender)
            
        
            ''' Обработка событий '''
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

            if event.object.payload.get('type') in CALLBACK_TYPES:
                vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload)
                    )

            elif event.object.payload.get('type') == 'what_is_password':
                text = passwords_info_str()
                vk.messages.edit(
                        peer_id=event.object.peer_id,
                        message=text,
                        conversation_message_id=event.object.conversation_message_id
                        )

            elif event.object.payload.get('type') == 'add_new_preset':
                text = 'Группа сохранена'
                db.change_new_group(user_id=event.object.user_id, new_group=True)
                vk.messages.edit(
                        peer_id=event.object.peer_id,
                        message=text,
                        conversation_message_id=event.object.conversation_message_id
                        )



def main_start():
    while True:
        try:
            try:
                main()
            except (requests.exceptions.ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError, socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError, vk_api.exceptions.ApiError):
                time.sleep(1)
                print('_______Timeout______')
        except Exception as ex:
            print(ex)
            time.sleep(1)
            print('_______Timeout______')


def mail_gather(seconds: int, time_str: str):
    while True:
        now_time = str(datetime.datetime.now().strftime("%H.%M"))
        try:
            group_online(vk_session=vk_session)
        except: 
            pass
        if now_time == time_str:
            break
        time.sleep(seconds)
    now_weekday = int(datetime.datetime.now().weekday())
    if now_weekday == 5:
        weekly_mail(sender=sender.sender, vk=vk)
    daily_mail(sender=sender.sender)
    time.sleep(70)
    mail_gather(seconds=seconds, time_str=time_str)


def run_parallel():
    p1 = multiprocessing.Process(target=mail_gather, args=[delay, time_str])
    p2 = multiprocessing.Process(target=main_start, args=[])

    p1.start()
    p2.start()

    p1.join()
    p2.join()


def table():
    create_tables()


if __name__ == '__main__':
    table()
    run_parallel()
