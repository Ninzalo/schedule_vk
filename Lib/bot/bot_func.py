# -*- coding: utf-8 -*-

import time

from Lib.bot.keyboards import *
from Lib.bot.elapsed_time import elapsed_time
from Lib.bot.display import Display
from Lib.bot.event_hint import Event_hint
from Lib.bot.stages import Pages
from Lib.bot.stages_names import Stages_names
from Lib.bot.mail import mail  
from Lib.bot.getter import get_all_weeks, get_schedule_path
from config import data_folder


class Bot_class:
    def __init__(self, sender, db, vk):
        self.db = db
        self.s = sender
        self.vk = vk
        self.data_folder = data_folder
        self.pages = Pages(sender=sender)
        self.display = Display(db=db, s=sender)
        self.sn = Stages_names()


    def old_messages(self, vk_session) -> int:
        amount_of_old_messages = 0
        all_users = self.db.get_users()
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
                        attachments = a['items'][0]['attachments']
                        )
                    Bot_class.bot(self, event=event)
            except Exception as ex:
                print(ex)
            time.sleep(0.5)
        return amount_of_old_messages

    @elapsed_time
    def bot(self, event: Event_hint):
        msg = event.msg
        id = event.id

        if '/s' == msg or 'начать' == msg:
            self.pages.start_page(id=id)
            return

        """ Проверка наличия файла с расписанием """
        form = self.db.get_form(user_id=id)
        group = self.db.get_group(user_id=id)
        fac = self.db.get_fac(user_id=id)
        if form != "None" and fac != "None" and group != "None":
            try:
                path = get_schedule_path(form=form, fac=fac, group=group)
                open(path)
            except:
                self.db.change_stage(user_id=id, stage=self.sn.START)
                self.db.null_schedule(user_id=id)
                text = 'Данные о группе удалены'
                keyboard = stage_start_keyboard()
                self.s.sender(id=id, text=text, keyboard=keyboard)
        del form, group, fac

        on_stage = self.db.get_stage(user_id=id)

        """ Кнопки на stage 100 """
        if on_stage == self.sn.HOME:
            """ Переход на stage 1 """
            if 'расписание' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 101 """
            elif 'другое' == msg:
                self.pages.other_page(id=id)

                """ Переход на stage 5 """
            elif 'расписание выбранной группы' == msg:
                if self.db.get_subgroup(user_id=id) != 'None':
                    self.pages.schedule_type_page(id=id, back_to_schedule_type_page=True)

            """ Кнопки на stage 101 """
        elif on_stage == self.sn.OTHER:
            """ Переход на stage 100 """
            if 'в начало' == msg:
                self.pages.home_page(id=id)

                """ Вывод списка преподавателей """
            elif 'преподаватели' == msg:
                self.display.teachers_display(id=id)

                """ Вывод информации о боте """
            elif 'информация о боте' in msg:
                self.display.bot_info_display(
                        button_actions=event.button_actions, 
                        id=id
                        )

                """ Переход на stage 102 """
            elif 'пароли' == msg:
                self.pages.passwords_page(id=id, event=event)

                """ Переход на stage 104 """
            elif 'рассылка расписания' == msg:
                self.pages.mail_page(id=id)

            """ Кнопки на stage 102 """
        elif on_stage == self.sn.PASSWORDS:
            """ Вывод паролей пользователя """
            if 'мои пароли' == msg:
                self.display.passwords_info_display(id=id)

                """ Переход на stage 101 """
            elif 'назад' == msg:
                self.pages.other_page(id=id)

                """ Удаление пароля """
            elif 'del ' in msg:
                entered_password = event.message.strip('del').strip('Del')
                entered_password = entered_password.strip()
                text = ''
                for pwd in self.db.get_passwords(user_id=id):
                    if pwd == entered_password:
                        success = self.db.del_password(user_id=id, password=pwd)
                        if success:
                            text = f'Пароль #{entered_password} удален'
                if text == '':
                    text = 'Пароль не найден'
                self.s.sender(id=id, text=text)

                """ Добавляем пароль пользователю """
            else:
                password = event.message
                if 'пароли' not in password.lower():
                    text, key = self.db.add_password(user_id=id, 
                            password=password)
                    self.s.sender(id=id, text=text)
                    if key == 1 | True:
                        """ Отправляем сообщение всем пользователям 
                        с password=password """
                        text = f'Пользователь @id{id} ввел пароль #{password}'
                        for user in self.db.get_all_users_with_pass(
                                password=password):
                            self.s.sender(id=user, text=text)

                        if self.db.get_privacy(password=password) == None:
                            """ Переход на stage 103 """
                            self.pages.setting_password_page(id=id)

            """ Кнопки на stage 103 """
        elif on_stage == self.sn.SETTING_PASSWORDS:
            """ Настройка приватности пароля пользователя """
            if 'приватная' == msg:
                self.db.change_stage(user_id=id, stage=self.sn.PASSWORDS)
                password = self.db.set_privacy(user_id=id, privacy=1)
                text = f'Пароль {password} успешно сохранен'
                keyboard = stage_passwords_keyboard()
                self.s.sender(id=id, text=text, keyboard=keyboard)
            elif 'открытая' == msg:
                self.db.change_stage(user_id=id, stage=self.sn.PASSWORDS)
                password = self.db.set_privacy(user_id=id, privacy=0)
                text = f'Пароль {password} успешно сохранен'
                keyboard = stage_passwords_keyboard()
                self.s.sender(id=id, text=text, keyboard=keyboard)

            """ Кнопки на stage 104 """
        elif on_stage == self.sn.MAIL:
            """ Переход на stage 101 """
            if 'назад' == msg:
                self.pages.other_page(id=id)

                """ Переключение ежедневной рассылки """
            elif 'ежедневная рассылка' == msg:
                if self.db.get_subgroup(user_id=id) != "None":
                    if self.db.get_daily_mail(user_id=id) == 0:
                        text = 'Включена ежедневная рассылка'
                        self.db.change_daily_mail(user_id=id, daily_mail=1)
                    else:
                        text = 'Ежедневная рассылка отключена'
                        self.db.change_daily_mail(user_id=id, daily_mail=0)
                    keyboard = stage_mail_keyboard(
                                daily_mail=self.db.get_daily_mail(user_id=id),
                                weekly_mail=self.db.get_weekly_mail(user_id=id)
                            )
                    self.s.sender(id=id, text=text, keyboard=keyboard)
                else:
                    text = 'Для начала выберите свою группу и подгруппу '\
                            'во вкладке "Расписание"!'
                    self.s.sender(id=id, text=text)

                """ Переключение еженедельной рассылки """
            elif 'еженедельная рассылка' == msg:
                if self.db.get_subgroup(user_id=id) != "None":
                    if self.db.get_weekly_mail(user_id=id) == 0:
                        text = 'Включена еженедельная рассылка'
                        self.db.change_weekly_mail(user_id=id, weekly_mail=1)
                    else:
                        text = 'Еженедельная рассылка отключена'
                        self.db.change_weekly_mail(user_id=id, weekly_mail=0)
                    keyboard = stage_mail_keyboard(
                                daily_mail=self.db.get_daily_mail(user_id=id),
                                weekly_mail=self.db.get_weekly_mail(user_id=id)
                            )
                    self.s.sender(id=id, text=text, keyboard=keyboard)
                else:
                    text = 'Для начала выберите свою группу и подгруппу '\
                            'во вкладке "Расписание"!'
                    self.s.sender(id=id, text=text)

                """ Кнопки на stage 1 """
        elif on_stage == self.sn.FORM:
            """ Обновляем формы обучения """
            if 'обновить формы' == msg:
                self.pages.form_page(id=id, update_forms=True)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id)

                """ Переход на stage 2 """
            else:
                self.pages.fac_page(id=id, msg=msg)

            """ Кнопки на stage 2 """
        elif on_stage == self.sn.FAC:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3 """
            else:
                self.pages.group_select_page(id=id, msg=msg, update_stage=True)

            """ Кнопки на stage 3 """
        elif on_stage == self.sn.GROUP_SELECT:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3.5 """
            elif 'сессия' == msg:
                self.pages.session_group_select_page(id=id, update_stage=True)

                """ Изменение group_page """
            elif '>' in msg:
                group_page = self.db.get_group_page(user_id=id)
                self.db.change_group_page(user_id=id, 
                        group_page=group_page + 1)
                self.pages.group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    self.db.change_group_page(user_id=id, group_page=1)
                else:
                    group_page = self.db.get_group_page(user_id=id)
                    self.db.change_group_page(user_id=id, 
                            group_page=group_page - 1)
                self.pages.group_select_page(id=id)

                """ Переход на stage 4 """
            else:
                self.pages.subgroup_page(id=id, msg=msg)

            """ Кнопки на stage 3.5 """
        elif on_stage == self.sn.SESSION_GROUP_SELECT:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3 """
            elif 'обычное расписание' == msg:
                self.pages.group_select_page(id=id, update_stage=True)

                """ Изменение session_group_page """
            elif '>' in msg:
                session_group_page = self.db.get_session_group_page(user_id=id)
                self.db.change_session_group_page(
                        user_id=id, 
                        session_group_page=session_group_page + 1)
                self.pages.session_group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    self.db.change_session_group_page(user_id=id, 
                            session_group_page=1)
                else:
                    session_group_page = self.db.get_session_group_page(user_id=id)
                    self.db.change_session_group_page(
                            user_id=id, 
                            session_group_page=session_group_page - 1)
                self.pages.session_group_select_page(id=id)

                """ Переход на stage 4 """
            else:
                self.pages.subgroup_page(id=id, session=True, msg=msg)

            """ Кнопки на stage 4 """
        elif on_stage == self.sn.SUBGROUP:
            """ Переход на stage 3 """
            if 'к выбору группы' == msg:
                self.pages.group_select_page(id=id, update_stage=True)

                """ Переход на stage 5 """
            else:
                self.pages.schedule_type_page(id=id, new_group=True, event=event, msg=msg)

            """ Кнопки на stage 5 """
        elif on_stage == self.sn.SCHEDULE_TYPE:
            """ Переход на stage 4 """
            if 'подгруппы' == msg:
                self.pages.subgroup_page(id=id)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id)

                """ Переход на stage 6 """
            elif 'расписание по дням' == msg:
                self.pages.date_select_page(id=id)

                """ Переход на stage 7 """
            elif 'расписание на неделю' == msg:
                self.pages.week_select_page(id=id)

                """ Переход на stage PRESETS """
            elif 'сохраненные группы' == msg:
                self.pages.preset_page(id=id)

            """ Кнопки на stage PRESETS """
        elif on_stage == self.sn.PRESETS:
            """ Переход на stage SCHEDULE_TYPE """
            if 'назад' == msg:
                self.pages.schedule_type_page(id=id, 
                        back_to_schedule_type_page=True)

            elif 'удалить' == msg:
                self.pages.preset_page(id=id, on_delete=True)

            elif 'к пресетам' == msg:
                self.pages.preset_page(id=id)

                """ Выбор или удаление пресета """
            else:
                self.display.presets_display(user_id=id, event=event)


            """ Кнопки на stage 6 """
        elif on_stage == self.sn.DATE_SELECT:
            """ Переход на stage 5 """
            if 'назад' == msg:
                self.pages.schedule_type_page(id=id, back_to_schedule_type_page=True)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id) 

                """ Обновление дат """
            elif 'обновить' == msg:
                self.pages.date_select_page(id=id, update=True)

                """ Переключение страниц на stage 6 """
            elif '>' in msg:
                date_page = self.db.get_date_page(user_id=id)
                self.db.change_date_page(user_id=id, 
                        date_page=date_page + 1)
                self.pages.date_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    self.db.change_date_page(user_id=id, date_page=1)
                else:
                    date_page = self.db.get_date_page(user_id=id)
                    self.db.change_date_page(user_id=id, 
                            date_page=date_page - 1)
                self.pages.date_select_page(id=id)

                """ Вывод расписания """
            else:
                self.display.schedule_display(id=id, msg=msg)

            """ Кнопки на stage 7 """
        elif on_stage == self.sn.WEEK_SELECT:
            """ Вывод текущей недели """
            if 'текущая неделя' == msg:
                type_of_week = 'now'
                text, doc, keyboard = get_all_weeks(
                        vk=self.vk, db=self.db, 
                        id=id, event=event, 
                        type_of_week=type_of_week,
                        stage_week_keyboard=stage_week_keyboard
                        )
                self.s.sender(id=id, text=text, preuploaded_doc=doc, 
                        keyboard=keyboard)

                """ Вывод ближайшей недели """
            elif 'ближайшая неделя' == msg:
                type_of_week = 'closest'
                text, doc, keyboard = get_all_weeks(
                        vk=self.vk, db=self.db, 
                        id=id, event=event, 
                        type_of_week=type_of_week,
                        stage_week_keyboard=stage_week_keyboard
                        )
                self.s.sender(id=id, text=text, preuploaded_doc=doc, 
                        keyboard=keyboard)

                """ Вывод предыдущей недели """
            elif '<' in msg:
                type_of_week = 'prev'
                text, doc, keyboard = get_all_weeks(
                        vk=self.vk, db=self.db, 
                        id=id, event=event, 
                        type_of_week=type_of_week,
                        stage_week_keyboard=stage_week_keyboard
                        )
                self.s.sender(id=id, text=text, preuploaded_doc=doc, 
                        keyboard=keyboard)

                """ Вывод следующей недели """
            elif '>' in msg:
                type_of_week = 'next'
                text, doc, keyboard = get_all_weeks(
                        vk=self.vk, db=self.db, 
                        id=id, event=event, 
                        type_of_week=type_of_week,
                        stage_week_keyboard=stage_week_keyboard
                        )
                self.s.sender(id=id, text=text, preuploaded_doc=doc, 
                        keyboard=keyboard)

                """ Переход на stage 8 """
            elif 'настройки' == msg:
                self.pages.settings_week_page(id=id)

                """ Переход на stage 5 """
            elif 'назад' == msg:
                self.pages.schedule_type_page(id=id, back_to_schedule_type_page=True)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id)

            """ Кнопки на stage 8 """
        elif on_stage == self.sn.SETTINGS_WEEK:
            """ Включение темного | светлого режима """
            if 'темный режим' == msg or 'светлый режим' == msg:
                self.pages.settings_week_page(id=id, edit='mode')

                """ Включение высокого | низкого качества """
            elif 'высокое качество' == msg or 'низкое качество' == msg:
                self.pages.settings_week_page(id=id, edit='quality')

                """ Переход на stage 7 """
            elif 'назад' == msg:
                self.pages.week_select_page(id=id)
        
        """ Рассылка от пользователей """
        mail(event=event, sender=self.s.sender, user_id=id)

        """ Сброс кнопок """
        if id == 290711560:
            if '/res' == msg:
                all_users = self.db.get_users()
                for user_id in all_users:
                    self.pages.reset_page(user_id=user_id)
