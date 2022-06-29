# -*- coding: utf-8 -*-

import vk_api
import datetime
import time
import socket
import urllib3
import os
import requests
import json
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import token_vk, group_id, db_path

from Lib.BotDB_Func import BotDB_Func
from Lib.bot_func import Bot_class
from Lib.sender import Sender
from Lib.event_hint import Event_hint


vk_session = vk_api.VkApi(token=token_vk)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

sender = Sender(vk_session=vk_session)
db = BotDB_Func(db_path=db_path)
bot_class = Bot_class(sender=sender)

data_folder = f'{os.getcwd()}\\data'


def main():
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
            bot_class.bot(event=event, vk=vk, db=db, s=sender, data_folder=data_folder)

if __name__ == '__main__':
    while True:
        main()
