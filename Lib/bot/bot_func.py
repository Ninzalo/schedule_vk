# -*- coding: utf-8 -*-

import time

from typing import Tuple

from Lib.bot.keyboards import stage_week_keyboard
# from Lib.bot.keyboards import stage_mail_keyboard

from Lib.bot.display import Display
from Lib.bot.event_hint import Event_hint
from Lib.bot.stages import Pages
from Lib.bot.stages_names import Stages_names
from Lib.bot.mail import mail, MailSettings
from Lib.bot.BotDB_Func import BotDB_Func, Notifications
# from Lib.bot.teachers import find_teacher
from Lib.bot.callback_messages import teacher_search_request

from Lib.bot.transfer import all_users_to_reset_page
from Lib.bot.transfer import deleted_group

from Lib.bot.passwords import Passwords

from Lib.bot.bot_return import Returns, error_return, fast_return
from config import data_folder


db = BotDB_Func()
notifications = Notifications()

class Bot_class:
    def __init__(self, vk) -> None:
        self.vk = vk
        self.data_folder = data_folder
        self.pages = Pages()
        self.display = Display()
        self.sn = Stages_names()
        self.passwords = Passwords()
        self.mail_settings = MailSettings()


    def old_messages(self, vk_session) -> Tuple[int, Returns]:
        amount_of_old_messages = 0
        messages = Returns()
        all_users = db.get_users()
        for user_id in all_users:
            try:
                post = {
                    'user_id': user_id,
                    'count': 1,
                    'offset': 0
                }
                a = vk_session.method('messages.getHistory', post)
                if a['items'][0]['out'] == 0:
                    amount_of_old_messages += 1
                    event = {
                        'message': a['items'][0]
                    }
                    event = Event_hint(
                        msg = a['items'][0]['text'].lower(),
                        message = a['items'][0]['text'],
                        id = a['items'][0]['from_id'],
                        peer_id = a['items'][0]['peer_id'],
                        button_actions = [],
                        attachments = a['items'][0]['attachments'])
                    messages.returns += Bot_class.bot(self, 
                        event=event).returns
            except Exception as ex:
                print(ex)
            time.sleep(0.5)
        return amount_of_old_messages, messages

    def bot(self, event: Event_hint) -> Returns:
        msg = event.msg
        id = event.id

        #""" Создание пользователя в базе """
        if '/s' == msg or 'начать' == msg:
            return self.pages.start_page(id=id)

        #""" Сброс кнопок """
        if id == 290711560:
            if '/res' == msg:
                return all_users_to_reset_page()

        #""" Проверка наличия файла с расписанием """
        success, deleted_group_result = deleted_group(user_id=id)
        if success == 0:
            return deleted_group_result 

        on_stage = db.get_stage(user_id=id)

        #""" Кнопки на stage 100 """
        if on_stage == self.sn.HOME:
            #""" Переход на stage 1 """
            if 'расписание' == msg:
                return self.pages.form_page(id=id)

                #""" Переход на stage OTHER """
            elif 'другое' == msg:
                return self.pages.other_page(id=id)

                #""" Переход на stage SHEDULE_TYPE """
            elif 'расписание выбранной группы' == msg:
                if db.get_subgroup(user_id=id) != 'None':
                    return self.pages.schedule_type_page(id=id, 
                        back_to_schedule_type_page=True)
                no_groups_added = 'У вас нет выбранных групп'
                return fast_return(user_id=id, text=no_groups_added)

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage OTHER """
        elif on_stage == self.sn.OTHER:
            #""" Переход на stage 100 """
            if 'в начало' == msg:
                return self.pages.home_page(id=id)

                #""" Переход на stage MESSAGES """
            elif 'сообщения' == msg:
                return self.pages.messages_page(id=id, event=event)

                #""" Переход на stage FIND_TEACHERS """
            elif 'поиск преподавателя' == msg:
                return self.pages.find_teacher_page(id=id)

                #""" Вывод списка преподавателей """
            elif 'преподаватели' == msg:
                return self.display.teachers_display(id=id)

                #""" Переход на stage GENERAL_SETTINGS """
            elif 'общие настройки' == msg:
                return self.pages.general_settings_page(user_id=id)

                #""" Вывод информации о боте """
            elif 'информация о боте' in msg:
                return self.display.bot_info_display(
                    button_actions=event.button_actions, id=id)

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage MESSAGES """
        elif on_stage == self.sn.MESSAGES:
            #""" Переход на stage PASSWORDS """
            if 'пароли' == msg:
                return self.pages.passwords_page(id=id, event=event)

                #""" Переход на stage HOME """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id)

                #""" Переход на stage OTHER """
            elif 'назад' == msg:
                return self.pages.other_page(id=id)
        
                #""" Рассылка от пользователей """
            else:
                return mail(event=event, user_id=id)


            #""" Кнопки на stage PASSWORDS """
        elif on_stage == self.sn.PASSWORDS:
            #""" Вывод паролей пользователя """
            if 'мои пароли' == msg:
                return self.display.passwords_info_display(id=id)

                #""" Переход на stage MESSAGES """
            elif 'назад' == msg:
                return self.pages.messages_page(id=id, event=event)

                #""" Удаление пароля """
            elif 'del ' in msg:
                return self.passwords.del_password(message=event.message, 
                    user_id=id)

                #""" Добавляем пароль пользователю """
            else:
                return self.passwords.add_password(message=event.message, 
                    user_id=id)

            #""" Кнопки на stage 103 """
        elif on_stage == self.sn.SETTING_PASSWORDS:
            #""" Настройка приватности пароля пользователя """
            if 'приватная' == msg:
                privacy = 1
                return self.pages.passwords_page(id=id, event=event,
                    set_privacy=privacy)
            elif 'открытая' == msg:
                privacy = 0
                return self.pages.passwords_page(id=id, event=event,
                    set_privacy=privacy)

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage MAIL """
        elif on_stage == self.sn.MAIL:
            """ Переход на stage SCHEDULE_TYPE """
            if 'назад' == msg:
                return self.pages.schedule_type_page(id=id, 
                    back_to_schedule_type_page=True)

                #""" Переключение ежедневной рассылки """
            elif 'ежедневная рассылка' == msg:
                return self.mail_settings.change_daily_mail(user_id=id)

                #""" Переключение еженедельной рассылки """
            elif 'еженедельная рассылка' == msg:
                return self.mail_settings.change_weekly_mail(user_id=id)

            else:
                return error_return(user_id=id)

                #""" Кнопки на stage FIND_TEACHERS """
        elif on_stage == self.sn.FIND_TEACHER:
            #""" Переход на stage OTHER """
            if 'назад' == msg:
                return self.pages.other_page(id=id)

                #""" Переход на stage HOME """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id)

                #""" Переход на stage TEACHER_SEARCH_SETTINGS """
            elif 'настройки' == msg:
                return self.pages.teacher_search_settings(user_id=id)

                #""" Поиск преподавателя """
            else:
                return teacher_search_request(user_id=id, name=msg)

                #""" Кнопки на stage TEACHER_SEARCH_SETTINGS """
        elif on_stage == self.sn.TEACHER_SEARCH_SETTINGS:
            #""" Переход на stage FIND_TEACHERS """
            if 'назад' == msg:
                return self.pages.find_teacher_page(id=id)

                #""" Изменение параметра full_search """
            elif 'постраничный поиск' == msg:
                return self.pages.teacher_search_settings(user_id=id,
                    edit='full_search')

            else:
                return error_return(user_id=id)

                #""" Кнопки на stage GENERAL_SETTINGS """
        elif on_stage == self.sn.GENERAL_SETTINGS:
            #""" Переход на stage HOME """
            if 'в начало' == msg:
                return self.pages.home_page(id=id)
                
                #""" Переход на stage OTHER """
            elif 'назад' == msg:
                return self.pages.other_page(id=id)

            elif 'рассылка обновлений' == msg:
                return self.pages.general_settings_page(user_id=id,
                    edit='notify')

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage 1 """
        elif on_stage == self.sn.FORM:
            #""" Обновляем формы обучения """
            if 'обновить формы' == msg:
                return self.pages.form_page(id=id, update_forms=True)

                #""" Переход на stage 100 """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id)

                #""" Переход на stage 2 """
            else:
                return self.pages.fac_page(id=id, msg=msg)

            #""" Кнопки на stage 2 """
        elif on_stage == self.sn.FAC:
            #""" Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                return self.pages.form_page(id=id)

                #""" Переход на stage 3 """
            else:
                return self.pages.group_select_page(id=id, msg=msg, 
                    update_stage=True)

            #""" Кнопки на stage 3 """
        elif on_stage == self.sn.GROUP_SELECT:
            #""" Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                return self.pages.form_page(id=id)

                #""" Переход на stage 3.5 """
            elif 'сессия' == msg:
                return self.pages.session_group_select_page(id=id, 
                    update_stage=True)

                #""" Изменение group_page """
            elif '>' in msg:
                group_page = db.get_group_page(user_id=id)
                db.change_group_page(user_id=id, 
                    group_page=group_page + 1)
                return self.pages.group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_group_page(user_id=id, group_page=1)
                else:
                    group_page = db.get_group_page(user_id=id)
                    db.change_group_page(user_id=id, 
                        group_page=group_page - 1)
                return self.pages.group_select_page(id=id)

                #""" Переход на stage SUBGROUP """
            else:
                return self.pages.subgroup_page(id=id, msg=msg)

            #""" Кнопки на stage SESSION_GROUP_SELECT """
        elif on_stage == self.sn.SESSION_GROUP_SELECT:
            #""" Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                return self.pages.form_page(id=id)

                #""" Переход на stage GROUP_SELECT """
            elif 'обычное расписание' == msg:
                return self.pages.group_select_page(id=id, 
                    update_stage=True)

                #""" Изменение session_group_page """
            elif '>' in msg:
                session_group_page = db.get_session_group_page(user_id=id)
                db.change_session_group_page(
                    user_id=id, 
                    session_group_page=session_group_page + 1)
                return self.pages.session_group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_session_group_page(user_id=id, 
                        session_group_page=1)
                else:
                    session_group_page = db.get_session_group_page(
                        user_id=id)
                    db.change_session_group_page(
                        user_id=id, 
                        session_group_page=session_group_page - 1)
                return self.pages.session_group_select_page(id=id)

                #""" Переход на stage 4 """
            else:
                return self.pages.subgroup_page(id=id, 
                    session=True, msg=msg)

            #""" Кнопки на stage 4 """
        elif on_stage == self.sn.SUBGROUP:
            #""" Переход на stage 3 """
            if 'к выбору группы' == msg:
                return self.pages.group_select_page(id=id, 
                    update_stage=True)

                #""" Переход на stage 5 """
            else:
                return self.pages.schedule_type_page(id=id, 
                    new_group=True, event=event, msg=msg)

            #""" Кнопки на stage SCHEDULE_TYPE """
        elif on_stage == self.sn.SCHEDULE_TYPE:
            #""" Переход на stage 4 """
            if 'подгруппы' == msg:
                return self.pages.subgroup_page(id=id)

                #""" Переход на stage 100 """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id)

                #""" Переход на stage 6 """
            elif 'расписание по дням' == msg:
                return self.pages.date_select_page(id=id)

                #""" Переход на stage 7 """
            elif 'расписание на неделю' == msg:
                return self.pages.week_select_page(id=id)

                #""" Переход на stage MAIL """
            elif 'рассылка расписания' == msg:
                return self.pages.mail_page(id=id)

                #""" Переход на stage PRESETS """
            elif 'сохраненные группы' == msg:
                return self.pages.preset_page(id=id)

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage PRESETS """
        elif on_stage == self.sn.PRESETS:
            #""" Переход на stage SCHEDULE_TYPE """
            if 'назад' == msg:
                return self.pages.schedule_type_page(id=id, 
                    back_to_schedule_type_page=True)

            elif 'удалить' == msg:
                return self.pages.preset_page(id=id, on_delete=True)

            elif 'к пресетам' == msg:
                return self.pages.preset_page(id=id)

                #""" Выбор или удаление пресета """
            else:
                return self.display.presets_display(user_id=id, 
                    event=event)


            #""" Кнопки на stage 6 """
        elif on_stage == self.sn.DATE_SELECT:
            #""" Переход на stage 5 """
            if 'назад' == msg:
                return self.pages.schedule_type_page(id=id, 
                    back_to_schedule_type_page=True)

                #""" Переход на stage 100 """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id) 

                #""" Обновление дат """
            elif 'обновить' == msg:
                return self.pages.date_select_page(id=id, update=True)

                #""" Переключение страниц на stage 6 """
            elif '>' in msg:
                date_page = db.get_date_page(user_id=id)
                db.change_date_page(user_id=id, 
                    date_page=date_page + 1)
                return self.pages.date_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_date_page(user_id=id, date_page=1)
                else:
                    date_page = db.get_date_page(user_id=id)
                    db.change_date_page(user_id=id, 
                        date_page=date_page - 1)
                return self.pages.date_select_page(id=id)

                #""" Вывод расписания """
            else:
                return self.display.schedule_display(id=id, msg=msg)

            #""" Кнопки на stage 7 """
        elif on_stage == self.sn.WEEK_SELECT:
            #""" Вывод текущей недели """
            if 'текущая неделя' == msg:
                type_of_week = 'now'
                return self.pages.week_change_page(vk=self.vk, 
                    user_id=id, event=event, type_of_week=type_of_week,
                    stage_week_keyboard=stage_week_keyboard)

                #""" Вывод ближайшей недели """
            elif 'ближайшая неделя' == msg:
                type_of_week = 'closest'
                return self.pages.week_change_page(vk=self.vk, 
                    user_id=id, event=event, type_of_week=type_of_week,
                    stage_week_keyboard=stage_week_keyboard)

                #""" Вывод предыдущей недели """
            elif '<' in msg:
                type_of_week = 'prev'
                return self.pages.week_change_page(vk=self.vk, 
                    user_id=id, event=event, type_of_week=type_of_week,
                    stage_week_keyboard=stage_week_keyboard)

                #""" Вывод следующей недели """
            elif '>' in msg:
                type_of_week = 'next'
                return self.pages.week_change_page(vk=self.vk, 
                    user_id=id, event=event, type_of_week=type_of_week,
                    stage_week_keyboard=stage_week_keyboard)

                #""" Переход на stage 8 """
            elif 'настройки' == msg:
                return self.pages.settings_week_page(id=id)

                #""" Переход на stage 5 """
            elif 'назад' == msg:
                return self.pages.schedule_type_page(id=id, 
                    back_to_schedule_type_page=True)

                #""" Переход на stage 100 """
            elif 'в начало' == msg:
                return self.pages.home_page(id=id)

            else:
                return error_return(user_id=id)

            #""" Кнопки на stage 8 """
        elif on_stage == self.sn.SETTINGS_WEEK:
            #""" Включение темного | светлого режима """
            if 'темный режим' == msg or 'светлый режим' == msg:
                return self.pages.settings_week_page(id=id, edit='mode')

                #""" Включение высокого | низкого качества """
            elif 'высокое качество' == msg or 'низкое качество' == msg:
                return self.pages.settings_week_page(id=id, edit='quality')

                #""" Переход на stage 7 """
            elif 'назад' == msg:
                return self.pages.week_select_page(id=id)

            else:
                return error_return(user_id=id)

        return error_return(user_id=id)
