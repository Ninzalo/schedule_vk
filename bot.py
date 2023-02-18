# -*- coding: utf-8 -*-

import time
import os
import vk_api
import datetime
import socket
from urllib3 import exceptions as urllib3_exceptions
import requests
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from Lib.bot.bot_return import Returns

from config import token_vk, group_id, delay, time_str

from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.bot_func import Bot_class
from Lib.bot.sender import Sender
from Lib.bot.event_hint import Event_hint
from Lib.bot.stages_names import Stages_names
from Lib.bot.callback_func import callback_func

from Lib.bot.mail import daily_mail, weekly_mail

from Lib.bot.group import group_online, wall_sender

from Lib.bot.table import create_tables

from Lib.start_files.create_files import bot_start_file
from Lib.start_files.create_files import schedule_start_file

import multiprocessing


while True:
    try:
        vk_session = vk_api.VkApi(token=token_vk)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, group_id)
        break
    except Exception as vk_connection_exception:
        print(f"__Timeout__ ({vk_connection_exception})")
        time.sleep(1)


sender = Sender(vk_session=vk_session)
sn = Stages_names()
db = BotDB_Func()
bot_class = Bot_class(vk=vk)


def main() -> None:
    start_time = datetime.datetime.now()
    amount_of_old_messages, messages = bot_class.old_messages(
        vk_session=vk_session
    )
    sender.sender(messages=messages)
    if amount_of_old_messages != 0:
        print(
            f"[INFO] {amount_of_old_messages} Old "
            f'message{"s" if amount_of_old_messages > 1 else ""} '
            f"answered in {datetime.datetime.now()-start_time}"
        )
    del start_time, amount_of_old_messages

    print("[INFO] Bot started")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            event = Event_hint(
                msg=event.object["message"]["text"].lower(),
                message=event.object["message"]["text"],
                id=event.object["message"]["from_id"],
                peer_id=event.object["message"]["peer_id"],
                button_actions=event.object["client_info"]["button_actions"],
                attachments=event.object["message"]["attachments"],
            )
            messages = bot_class.bot(event=event)
            sender.sender(messages=messages)

            """ Обработка постов """
        elif event.type == VkBotEventType.WALL_POST_NEW:
            id_ = event.object["id"]
            owner_id_ = event.group_id
            wall_id = f"wall-{owner_id_}_{id_}"
            messages = wall_sender(post=wall_id)
            sender.sender(messages=messages)

            """ Обработка событий """
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            returns = callback_func(event=event, vk=vk)
            if returns is not None:
                sender.sender(messages=returns)


def main_start() -> None:
    while True:
        try:
            try:
                main()
            except (
                requests.exceptions.ReadTimeout,
                socket.timeout,
                urllib3_exceptions.ReadTimeoutError,
                socket.gaierror,
                urllib3_exceptions.NewConnectionError,
                urllib3_exceptions.MaxRetryError,
                requests.exceptions.ConnectionError,
                vk_api.exceptions.ApiError,
            ):
                time.sleep(1)
                print("_______Timeout______")
        except Exception as ex:
            print(ex)
            time.sleep(1)
            print("_______Timeout______")


def mail_gather(seconds: int, time_str: str) -> None:
    messages = Returns()
    while True:
        now_time = str(datetime.datetime.now().strftime("%H.%M"))
        print(now_time)
        # try:
        # group_online(vk_session=vk_session)
        # except:
        # pass
        if now_time == time_str:
            break
        time.sleep(seconds)
    now_weekday = int(datetime.datetime.now().weekday())
    if now_weekday == 5:
        messages.returns += weekly_mail(vk=vk).returns
    messages.returns += daily_mail().returns
    sender.sender(messages=messages)
    time.sleep(70)
    mail_gather(seconds=seconds, time_str=time_str)


def run_parallel() -> None:
    p1 = multiprocessing.Process(target=mail_gather, args=[delay, time_str])
    p2 = multiprocessing.Process(target=main_start, args=[])

    p1.start()
    p2.start()

    p1.join()
    p2.join()


def table() -> None:
    create_tables()


if __name__ == "__main__":
    bot_start_file(path=os.getcwd())
    schedule_start_file(path=os.getcwd())
    table()
    run_parallel()
