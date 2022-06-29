# -*- coding: utf-8 -*-

import os
from Lib.keyboards import *
from Lib.elapsed_time import elapsed_time
from Lib.display import display_schedule
from Lib.stages_func import *
from Lib.event_hint import Event_hint
from Lib.stages import Pages

class Bot_class:
    def __init__(self, sender):
        self.pages = Pages(sender=sender)

    @elapsed_time
    def bot(self, event: Event_hint, vk, db, s, data_folder: str):
        msg = event.msg

        id = event.id

        """ Проверка наличия файла с расписанием """
        for user in db.get_users():
            form = db.get_form(user_id=user)
            group = db.get_group(user_id=user)
            fac = db.get_fac(user_id=user)
            if form != "None" and fac != "None" and group != "None":
                try:
                    path = f'{data_folder}\\{form}\\{fac}\\data\\schedule\\'\
                            f'schedule_{group}.json'
                    open(path)
                except:
                    db.change_stage(user_id=user, stage=0)
                    db.null_schedule(user_id=user)
                    text = 'Данные о группе удалены'
                    keyboard = stage_start_keyboard()
                    s.sender(id=user, text=text, keyboard=keyboard)

        if '/s' == msg or 'начать' == msg:
            db.start(user_id=id)
            text = f'Привет😉\nДанный бот дублирует информацию о расписании '\
                    'с официального сайта МГТУ ГА '\
                    '( обновление информации в боте происходит каждую среду )'\
                    f'\nВся информация собрана из открытых источников\n\n'
            s.sender(id=id, text=text)

            self.pages.home_page(id=id, null=True)
            return

        on_stage = db.get_stage(user_id=id)

        """ Кнопки на stage 100 """
        if on_stage == 100:
            """ Переход на stage 1 """
            if 'расписание' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 101 """
            elif 'другое' == msg:
                self.pages.other_page(id=id)

                """ Переход на stage 5 """
            elif 'расписание выбранной группы' == msg:
                if db.get_subgroup(user_id=id) != 'None':
                    self.pages.schedule_type_page(id=id)

            """ Кнопки на stage 101 """
        elif on_stage == 101:
            """ Переход на stage 100 """
            if 'в начало' == msg:
                self.pages.home_page(id=id)

                """ Вывод списка преподавателей """
            elif 'преподаватели' == msg:
                if 'teachers' in db.get_passwords(user_id=id):
                    path = f'{os.getcwd()}\\users_data\\teachers.json'
                    with open(path, 'r', encoding='utf-8') as teachers:
                        list_of_teachers = json.load(teachers)
                    text = ""
                    for teacher in list_of_teachers:
                        text += f'Имя: {teacher["name"]}\n'\
                                'Телефон: {teacher["phone"]}\n'\
                                'Почта: {teacher["mail"]}\n\n'
                    s.sender(id=id, text=text)
                else: 
                    text = 'У вас нет доступа для получения '\
                            'информации о преподавателях'
                    s.sender(id=id, text=text)

                    """ Вывод информации о боте """
            elif 'информация о боте' in msg:
                if 'callback' in event.button_actions:
                    text = 'Данный бот дублирует информацию о расписании с '\
                            'официального сайта МГТУ ГА ' \
                            '( обновление информации в боте '\
                            'происходит каждую среду )\n' \
                            'Вся информация собрана из открытых источников\n\n' \
                            'Вопросы и предложения писать разработчику '\
                            'или в обсуждении:'
                    settings = dict(inline=True)
                    inline_keyboard = VkKeyboard(**settings)
                    inline_keyboard.add_callback_button(
                            label='Сообщение разработчику', 
                            color=VkKeyboardColor.POSITIVE, 
                            payload={
                                'type': 'open_link', 
                                'link': 'https://vk.com/im?media=&sel=478270913'
                                }
                            )
                    inline_keyboard.add_line()
                    inline_keyboard.add_callback_button(
                            label='Обсуждение', 
                            color=VkKeyboardColor.POSITIVE, 
                            payload={
                                'type': 'open_link', 
                                'link': 'https://vk.com/topic-210110232_48270692'
                                }
                            )
                    s.sender(id=id, text=text, inline_keyboard=inline_keyboard)
                else:
                    text = 'Данный бот дублирует информацию о расписании с '\
                            'официального сайта МГТУ ГА ' \
                            '( обновление информации в боте '\
                            'происходит каждую среду )\n' \
                            'Вся информация собрана из открытых источников\n\n' \
                            'Вся информация собрана из открытых источников\n\n'\
                            'Вопросы и предложения писать '\
                            'разработчику - @id478270913 или в '\
                            'обсуждении https://vk.com/topic-210110232_48270692'
                    s.sender(id=id, text=text)

                """ Переход на stage 102 """
            elif 'пароли' == msg:
                self.pages.passwords_page(id=id, event=event)

                """ Переход на stage 104 """
            elif 'рассылка расписания' == msg:
                self.pages.mail_page(id=id)

            """ Кнопки на stage 102 """
        elif on_stage == 102:
            """ Вывод паролей пользователя """
            if 'мои пароли' == msg:
                if not len(db.get_passwords(user_id=id)):
                    text = ''
                    for password in db.get_passwords(user_id=id):
                        creator = db.get_creator(password=password)
                        privacy = db.get_privacy(password=password)
                        text += f'✅Пароль: {password}\nСоздатель: @id{creator}\n'\
                                f'Приватность: {"+" if privacy == 1 else "-"}\n\n'
                    s.sender(id=id, text=text)
                else:
                    text = 'Нет сохраненных паролей'
                    s.sender(id=id, text=text)

                """ Переход на stage 101 """
            elif 'назад' == msg:
                self.pages.other_page(id=id)

                """ Удаление пароля """
            elif 'del ' in msg:
                password = event.message.strip('del').strip('Del')
                password = password.strip()
                text = ''
                for pwd in db.get_passwords(user_id=id):
                    if pwd == password:
                        success = db.del_password(user_id=id, password=pwd)
                        if success:
                            text = f'Пароль {password} удален'
                if text == '':
                    text = 'Пароль не найден'
                s.sender(id=id, text=text)

                """ Добавляем пароль пользователю """
            else:
                password = event.message
                if 'пароли' not in password.lower():
                    text, key = db.add_password(user_id=id, password=password)
                    s.sender(id=id, text=text)
                    if key == 1 | True:
                        """ Отправляем сообщение всем пользователям с password=password """
                        text = f'Пользователь @id{id} ввел пароль {password}'
                        for user in db.get_all_users_with_pass(password=password):
                            s.sender(id=user, text=text)

                        """ Переход на stage 103 """
                        text = f'Выберите параметр приватности рассылки:\n'\
                                'Приватная -> делать рассылку может только '\
                                'создатель\n'\
                                'Открытая -> делать рассылку могут все '\
                                'пользователи, которые ввели пароль'
                        db.change_stage(user_id=id, stage=103)
                        keyboard = stage_setting_passwords_keyboard()
                        s.sender(id=id, text=text, keyboard=keyboard)

            """ Кнопки на stage 103 """
        elif on_stage == 103:
            if 'приватная' == msg:
                password = db.set_privacy(user_id=id, privacy=1)
                text = f'Пароль {password} успешно сохранен'
                keyboard = stage_passwords_keyboard()
                s.sender(id=id, text=text, keyboard=keyboard)
            elif 'открытая' == msg:
                password = db.set_privacy(user_id=id, privacy=0)
                text = f'Пароль {password} успешно сохранен'
                keyboard = stage_passwords_keyboard()
                s.sender(id=id, text=text, keyboard=keyboard)

            """ Кнопки на stage 104 """
        elif on_stage == 104:
            """ Переход на stage 101 """
            if 'назад' == msg:
                self.pages.other_page(id=id)

                """ Переключение ежедневной рассылки """
            elif 'ежедневная рассылка' == msg:
                if db.get_subgroup(user_id=id) == "None":
                    if db.get_daily_mail(user_id=id) == 0:
                        text = 'Включена ежедневная рассылка'
                        db.change_daily_mail(user_id=id, daily_mail=1)
                    else:
                        text = 'Ежедневная рассылка отключена'
                        db.change_daily_mail(user_id=id, daily_mail=0)
                    keyboard = stage_mail_keyboard(
                                daily_mail=db.get_daily_mail(user_id=id),
                                weekly_mail=db.get_weekly_mail(user_id=id)
                            )
                    s.sender(id=id, text=text, keyboard=keyboard)
                else:
                    text = 'Для начала выберите свою группу и подгруппу '\
                            'во вкладке "Расписание"!'
                    s.sender(id=id, text=text)

                """ Переключение еженедельной рассылки """
            elif 'еженедельная рассылка' == msg:
                if db.get_subgroup(user_id=id) == "None":
                    if db.get_weekly_mail(user_id=id) == 0:
                        text = 'Включена еженедельная рассылка'
                        db.change_weekly_mail(user_id=id, weekly_mail=1)
                    else:
                        text = 'Еженедельная рассылка отключена'
                        db.change_weekly_mail(user_id=id, weekly_mail=0)
                    keyboard = stage_mail_keyboard(
                                daily_mail=db.get_daily_mail(user_id=id),
                                weekly_mail=db.get_weekly_mail(user_id=id)
                            )
                    s.sender(id=id, text=text, keyboard=keyboard)
                else:
                    text = 'Для начала выберите свою группу и подгруппу '\
                            'во вкладке "Расписание"!'
                    s.sender(id=id, text=text)

                """ Кнопки на stage 1 """
        elif on_stage == 1:
            """ Обновляем формы обучения """
            if 'обновить формы' == msg:
                self.pages.form_page(id=id, update_forms=True)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                db.null_schedule(user_id=id)
                self.pages.home_page(id=id)

                """ Переход на stage 2 """
            else:
                self.pages.fac_page(id=id, msg=msg)

            """ Кнопки на stage 2 """
        elif on_stage == 2:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3 """
            else:
                self.pages.group_select_page(id=id, msg=msg)

            """ Кнопки на stage 3 """
        elif on_stage == 3:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3.5 """
            elif 'сессия' == msg:
                self.pages.session_group_select_page(id=id, update_stage=True)

                """ Изменение group_page """
            elif '>' in msg:
                group_page = db.get_group_page(user_id=id)
                db.change_group_page(user_id=id, group_page=group_page + 1)
                self.pages.group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_group_page(user_id=id, group_page=1)
                else:
                    group_page = db.get_group_page(user_id=id)
                    db.change_group_page(user_id=id, group_page=group_page - 1)
                self.pages.group_select_page(id=id)

                """ Переход на stage 4 """
            else:
                self.pages.subgroup_page(id=id, msg=msg)

            """ Кнопки на stage 3.5 """
        elif on_stage == 3.5:
            """ Переход на stage 1 """
            if 'к выбору формы обучения' == msg:
                self.pages.form_page(id=id)

                """ Переход на stage 3 """
            elif 'обычное расписание' == msg:
                self.pages.group_select_page(id=id, update_stage=True)

                """ Изменение session_group_page """
            elif '>' in msg:
                session_group_page = db.get_session_group_page(user_id=id)
                db.change_session_group_page(
                        user_id=id, 
                        session_group_page=session_group_page + 1)
                self.pages.session_group_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_session_group_page(user_id=id, session_group_page=1)
                else:
                    session_group_page = db.get_session_group_page(user_id=id)
                    db.change_session_group_page(
                            user_id=id, 
                            session_group_page=session_group_page - 1)
                self.pages.session_group_select_page(id=id)

                """ Переход на stage 4 """
            else:
                self.pages.subgroup_page(id=id, session=True, msg=msg)

            """ Кнопки на stage 4 """
        elif on_stage == 4:
            """ Переход на stage 3 """
            if 'к выбору группы' == msg:
                self.pages.group_select_page(id=id, update_stage=True)

                """ Переход на stage 5 """
            else:
                self.pages.schedule_type_page(id=id, msg=msg)

            """ Кнопки на stage 5 """
        elif on_stage == 5:
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

            """ Кнопки на stage 6 """
        elif on_stage == 6:
            """ Переход на stage 5 """
            if 'назад' == msg:
                self.pages.schedule_type_page(id=id)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id) 

                """ Обновление дат """
            elif 'обновить' == msg:
                self.pages.date_select_page(id=id, update=True)

                """ Переключение страниц на stage 6 """
            elif '>' in msg:
                date_page = db.get_date_page(user_id=id)
                db.change_date_page(user_id=id, date_page=date_page + 1)
                self.pages.date_select_page(id=id)
            elif '<' in msg:
                if '< стр 1' == msg:
                    db.change_date_page(user_id=id, date_page=1)
                else:
                    date_page = db.get_date_page(user_id=id)
                    db.change_date_page(user_id=id, date_page=date_page - 1)
                self.pages.date_select_page(id=id)

                """ Вывод расписания """
            else:
                form = db.get_form(user_id=id)
                fac = db.get_fac(user_id=id)
                group = db.get_group(user_id=id)
                subgroup = db.get_subgroup(user_id=id)
                path = f'{data_folder}\\{form}\\{fac}\\data'\
                        f'\\schedule\\schedule_{group}.json'
                with open(path) as f:
                    data = json.load(f)
                for date in data:
                    if date['date'] == msg.split(' ')[1]:
                        try:
                            if date['date'] == msg.split(' ')[1]:
                                if date['lessons'][0]['day_of_week'] in msg:
                                    text = display_schedule(
                                            data=date, 
                                            subgroup=subgroup, 
                                            date=date['date'])
                                    s.sender(id=id, text=text)
                        except:
                            print(124)
                            pass

            """ Кнопки на stage 7 """
        elif on_stage == 7:
            """ Вывод текущей недели """
            if 'текущая неделя' == msg:
                type_of_week = 'now'
                text, doc, keyboard = get_all_weeks(
                        data_folder=data_folder, 
                        vk=vk, 
                        db=db, 
                        id=id, 
                        event=event, 
                        type_of_week=type_of_week
                        )
                s.sender(id=id, text=text, preuploaded_doc=doc, keyboard=keyboard)

                """ Вывод ближайшей недели """
            elif 'ближайшая неделя' == msg:
                type_of_week = 'closest'
                text, doc, keyboard = get_all_weeks(
                        data_folder=data_folder, 
                        vk=vk, 
                        db=db, 
                        id=id, 
                        event=event, 
                        type_of_week=type_of_week
                        )
                s.sender(id=id, text=text, preuploaded_doc=doc, keyboard=keyboard)

                """ Вывод предыдущей недели """
            elif '<' in msg:
                type_of_week = 'prev'
                text, doc, keyboard = get_all_weeks(
                        data_folder=data_folder, 
                        vk=vk, 
                        db=db, 
                        id=id, 
                        event=event, 
                        type_of_week=type_of_week
                        )
                s.sender(id=id, text=text, preuploaded_doc=doc, keyboard=keyboard)

                """ Вывод следующей недели """
            elif '>' in msg:
                type_of_week = 'next'
                text, doc, keyboard = get_all_weeks(
                        data_folder=data_folder, 
                        vk=vk, 
                        db=db, 
                        id=id, 
                        event=event, 
                        type_of_week=type_of_week
                        )
                s.sender(id=id, text=text, preuploaded_doc=doc, keyboard=keyboard)

                """ Переход на stage 8 """
            elif 'настройки' == msg:
                self.pages.settings_week_page(id=id)

                """ Переход на stage 5 """
            elif 'назад' == msg:
                self.pages.schedule_type_page(id=id)

                """ Переход на stage 100 """
            elif 'в начало' == msg:
                self.pages.home_page(id=id)

            """ Кнопки на stage 8 """
        elif on_stage == 8:
            """ Включение темного режима """
            if 'темный режим' == msg:
                db.change_mode(user_id=id)
                mode = db.get_mode(user_id=id)
                quality = db.get_quality(user_id=id)
                text = 'Выбран темный режим'
                keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
                s.sender(id=id, text=text, keyboard=keyboard)

                """ Включение светлого режима """
            elif 'светлый режим' == msg:
                db.change_mode(user_id=id)
                mode = db.get_mode(user_id=id)
                quality = db.get_quality(user_id=id)
                text = 'Выбран светлый режим'
                keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
                s.sender(id=id, text=text, keyboard=keyboard)

                """ Включение высокого качества """
            elif 'высокое качество' == msg:
                db.change_quality(user_id=id)
                mode = db.get_mode(user_id=id)
                quality = db.get_quality(user_id=id)
                text = 'Выбрано высокое качество картинок'
                keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
                s.sender(id=id, text=text, keyboard=keyboard)

                """ Включение низкого качества """
            elif 'низкое качество' == msg:
                db.change_quality(user_id=id)
                mode = db.get_mode(user_id=id)
                quality = db.get_quality(user_id=id)
                text = 'Выбрано низкое качество картинок'
                keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
                s.sender(id=id, text=text, keyboard=keyboard)

                """ Переход на stage 7 """
            elif 'назад' == msg:
                self.pages.week_select_page(id=id)
