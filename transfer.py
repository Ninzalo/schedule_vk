# -*- coding: utf-8 -*-

import os
import json
from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.elapsed_time import elapsed_time
from config import db_path

db = BotDB_Func(db_path=db_path)

@elapsed_time
def data_fetch(user: dict):
    """ Получение основной информации из файла """
    user_id = user['user_id']
    print(f'User_id - {user_id}')
    user_quality = user['quality']
    user_mode = user['mode']
    user_daily_mail = user['daily_mail']
    user_weekly_mail = user['weekly_mail']
    user_passwords_info = user['passwords']

    """ Добавление данных в базу """
    db.start(user_id=user_id)
    db.change_daily_mail(user_id=user_id, daily_mail=user_daily_mail)
    db.change_weekly_mail(user_id=user_id, weekly_mail=user_weekly_mail)

    if user_mode == 'day':
        db.change_mode(user_id=user_id)
    if user_quality == 2:
        db.change_quality(user_id=user_id)

    """ Добавление паролей пользователю """
    for password in user_passwords_info:
        user_password = password['password']
        creator_id = password['creator']
        privacy = password['private']
        print(f'Password - {user_password} | Creator - {creator_id} | '\
                f'Privacy - {privacy}')

        db.add_password(user_id=user_id, password=user_password)
        db.set_privacy(user_id=user_id, privacy=privacy)
        db._set_creator(creator_id=creator_id, password=user_password)

@elapsed_time
def update_users_from_file():
    users_path = f'D:\\Programs\\Python\\TestBot\\Schedule_vk\\users_data\\users.json'
    with open(users_path, 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    for user in users_data:
        data_fetch(user=user)


def main():
    update_users_from_file()


if __name__ == '__main__':
    main()
