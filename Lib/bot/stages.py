from typing import List, Type

from vk_api import keyboard

from Lib.bot.event_hint import Event_hint

from Lib.bot.BotDB_Func import BotDB_Func

from Lib.bot.keyboards import (stage_start_keyboard, stage_home_keyboard,
    stage_other_keyboard, stage_passwords_keyboard, 
    stage_setting_passwords_keyboard, stage_mail_keyboard, 
    stage_preset_keyboard, stage_form_keyboard, 
    stage_fac_keyboard, stage_settings_week_keyboard,
    stage_group_keyboard, stage_session_group_keyboard, 
    stage_subgroup_keyboard, stage_schedule_type_keyboard,
    stage_date_keyboard, stage_week_keyboard,
    stage_find_teacher_keyboard)

from Lib.bot.keyboards import messages_keyboard

from Lib.bot.inline_keyboards import add_new_preset
from Lib.bot.inline_keyboards import passwords_desc
from Lib.bot.inline_keyboards import short_description
from Lib.bot.inline_keyboards import message_example

from Lib.bot.stages_names import Stages_names

from Lib.bot.output_texts import passwords_info_str
from Lib.bot.output_texts import settings_password_str
from Lib.bot.output_texts import start_message_str
from Lib.bot.output_texts import messages_str

from Lib.bot.bot_getter import get_forms
from Lib.bot.bot_getter import get_facs
from Lib.bot.bot_getter import get_session_groups
from Lib.bot.bot_getter import get_groups
from Lib.bot.bot_getter import get_subgroups

from config import db_path

db = BotDB_Func(db_path=db_path)

class Pages:
    def __init__(self, sender):
        self.s = sender
        self.sn = Stages_names()
    

    def reset_page(self, user_id: int) -> None:
        text = f"Кнопки сброшены\nОбновление!\n[ Информацию об "\
            f"обновлении искать на странице сообщества ]"\
            f"\nНажмите кнопку 'Начать'"
        keyboard = stage_start_keyboard()
        self.s.sender(id=user_id, text=text, keyboard=keyboard)


    def start_page(self, id:int) -> None:
        db.start(user_id=id)
        text = start_message_str()
        self.s.sender(id=id, text=text)
        text = f'Хотите подробнее узнать о функционале бота?'
        keyboard = short_description()
        self.s.sender(id=id, text=text, inline_keyboard=keyboard)
        Pages.home_page(self, id=id, null_user=True)


    def home_page(self, id: int, null_user:bool|None=None) -> None:
        db.change_stage(user_id=id, stage=self.sn.HOME)
        if null_user is not None:
            db.null_user(user_id=id)
        subgroup = db.get_subgroup(user_id=id)
        text = "Выберите: "
        keyboard = stage_home_keyboard(subgroup=subgroup)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def other_page(self, id: int) -> None:
        db.change_stage(user_id=id, stage=self.sn.OTHER)
        text = 'Выберите: '
        can_get_teachers = False
        if 'teachers' in db.get_passwords(user_id=id):
            can_get_teachers = True
        keyboard = stage_other_keyboard(can_get_teachers=can_get_teachers)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def messages_page(self, id: int, event) -> None:
        db.change_stage(user_id=id, stage=self.sn.MESSAGES)
        if 'callback' in event.button_actions:
            text = f'Формат сообщения: <пароль> <сообщение>'
            inline_keyboard = message_example()
            self.s.sender(id=id, text=text, 
                inline_keyboard=inline_keyboard)
        else:
            text = messages_str()
            self.s.sender(id=id, text=text)
        text = f'Введите сообщение:'
        keyboard = messages_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)
        

    def passwords_page(self, id: int, event) -> None:
        db.change_stage(user_id=id, stage=self.sn.PASSWORDS)
        if 'callback' in event.button_actions:
            text = 'Что такое код-пароль?'
            inline_keyboard = passwords_desc()
            self.s.sender(id=id, text=text, 
                inline_keyboard=inline_keyboard)
        else:
            text = passwords_info_str() 
            self.s.sender(id=id, text=text)
        text = 'Введите пароль:'
        keyboard = stage_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def setting_password_page(self, id: int) -> None:
        db.change_stage(user_id=id, stage=self.sn.SETTING_PASSWORDS)
        text = settings_password_str()
        keyboard = stage_setting_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def mail_page(self, id: int) -> None:
        db.change_stage(user_id=id, stage=self.sn.MAIL)
        daily_mail = db.get_daily_mail(user_id=id)
        weekly_mail = db.get_weekly_mail(user_id=id)
        text = 'Включите/выключите рассылку расписания:'
        keyboard = stage_mail_keyboard(
                daily_mail=daily_mail, 
                weekly_mail=weekly_mail
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def find_teacher_page(self, id: int) -> None:
        db.change_stage(user_id=id, stage=self.sn.FIND_TEACHER)
        text = 'Введите фамилию преподавателя:'
        keyboard = stage_find_teacher_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def preset_page(self, id: int, on_delete: bool|None=None) -> None:
        db.change_stage(user_id=id, stage=self.sn.PRESETS)
        if on_delete is True:
            db.change_on_delete(user_id=id, on_delete=1)
        else:
            db.change_on_delete(user_id=id, on_delete=0)
        text = 'Выберите одну из сохраненных групп: '
        presets = db.get_user_preset_data(user_id=id)
        chosen_preset = db.get_preset(user_id=id)
        keyboard = stage_preset_keyboard(presets=presets, 
                chosen_preset=chosen_preset, on_delete=on_delete)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def form_page(self, id: int, update_forms: bool|None = None) -> None:
        db.add_new_group(user_id=id)
        text = "Выберите одну из форм обучения:"
        keyboard, error = stage_form_keyboard()
        if error == 1:
            text = 'Нет расписания :c'
        else:
            if update_forms is None:
                db.change_stage(user_id=id, stage=self.sn.FORM)
                db.null_schedule(user_id=id)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def fac_page(self, id: int, msg: str) -> None:
        forms = get_forms()
        for form in forms:
            if form.lower() == msg:
                db.change_stage(user_id=id, stage=self.sn.FAC)
                db.change_form(user_id=id, form=form)
                text = 'Выберите один из факультетов:'
                keyboard = stage_fac_keyboard(form=form)
                self.s.sender(id=id, text=text, keyboard=keyboard)

    def group_select_page(self, id: int, msg: None|str = None, 
            update_stage: bool|None = None) -> None:
        form = db.get_form(user_id=id)
        group_page = db.get_group_page(user_id=id)
        fac = ''
        if msg is not None:
            facs = get_facs(form=form)
            for fac in facs:
                if fac.lower() == msg:
                    db.change_fac(user_id=id, fac=fac)
                    db.change_stage(user_id=id, stage=self.sn.GROUP_SELECT)
                    break
        else:
            if update_stage is not None:
                db.change_stage(user_id=id, stage=self.sn.GROUP_SELECT)
            db.del_group(user_id=id)
            db.del_subgroup(user_id=id)
            fac = db.get_fac(user_id=id)
        text = f'Выберите одну из групп:\nПоказана страница {group_page}'
        keyboard = stage_group_keyboard(
                form=form, 
                fac=fac, 
                group_page=group_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def session_group_select_page(self, id: int, 
            update_stage:bool|None = None) -> None:
        if update_stage is not None:
            db.change_stage(user_id=id, stage=self.sn.SESSION_GROUP_SELECT)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        session_group_page = db.get_session_group_page(user_id=id)
        text = f'Выберите одну из групп:\nПоказана страница {session_group_page}'
        keyboard = stage_session_group_keyboard(
                form=form, 
                fac=fac, 
                session_group_page=session_group_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def subgroup_page(self, id: int, session:None|bool=None, 
            msg:None|str=None) -> None:
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = ''
        if msg is not None:
            if session == True:
                groups = get_session_groups(form=form, fac=fac)
            else:
                groups = get_groups(form=form, fac=fac)
            for group in groups:
                if group.lower() == msg:
                    db.change_stage(user_id=id, stage=self.sn.SUBGROUP)
                    db.change_group(user_id=id, group=group)
                    break
                else:
                    group = ''
        else:
            db.change_stage(user_id=id, stage=self.sn.SUBGROUP)
            db.del_subgroup(user_id=id)
            group = db.get_group(user_id=id)
        if group != '':
            text = 'Выберите подгруппу:'
            keyboard = stage_subgroup_keyboard(
                    form=form, 
                    fac=fac, 
                    group=group
                    )
            self.s.sender(id=id, text=text, keyboard=keyboard)


    def schedule_type_page(self, id: int, new_group: bool|None = None, 
            back_to_schedule_type_page: bool|None = None,
            event: Event_hint|None = None, msg: str|None = None) -> None:
        db.change_on_delete(user_id=id, on_delete=0)
        if back_to_schedule_type_page is True:
            if db.get_new_group(user_id=id):
                db.change_new_group(user_id=id, new_group=True)
        else:
            db.change_new_group(user_id=id, new_group=False)
        if msg is not None:
            form = db.get_form(user_id=id)
            fac = db.get_fac(user_id=id)
            group = db.get_group(user_id=id)
            all_subgroups = get_subgroups(
                    form=form, 
                    fac=fac, 
                    group=group
                    )
            for subgroup in range(1, all_subgroups + 1):
                if str(subgroup).lower() == msg:
                    db.change_subgroup(user_id=id, subgroup=str(subgroup))
        db.change_stage(user_id=id, stage=self.sn.SCHEDULE_TYPE)
        if new_group is not None:
            user_presets = db.get_user_preset_data(user_id=id)
            form = db.get_form(user_id=id)
            fac = db.get_fac(user_id=id)
            group = db.get_group(user_id=id)
            subgroup = db.get_subgroup(user_id=id)
            is_ok = 0
            for (_, preset_form, preset_fac, preset_group, 
                preset_subgroup) in user_presets:
                if (preset_form == form and preset_fac == fac
                and preset_group == group 
                and str(preset_subgroup) == str(subgroup)):
                    is_ok += 1
            if is_ok < 2:
                if 'callback' in event.button_actions:
                    if len(db.get_all_user_presets(user_id=id)) < 5:
                        text = 'Сохранить группу?'
                        inline_keyboard = add_new_preset()
                        self.s.sender(id=id, text=text, 
                                inline_keyboard=inline_keyboard)
        text = 'Выберите: '
        keyboard = stage_schedule_type_keyboard(user_id=id)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def date_select_page(self, id: int, update:bool|None=None) -> None:
        db.change_stage(user_id=id, stage=self.sn.DATE_SELECT)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = db.get_group(user_id=id)
        date_page = db.get_date_page(user_id=id)
        if update is not None:
            text = 'Даты обновлены'
        else:
            text = f'Выберите дату:\nПоказана страница {date_page}'
        keyboard = stage_date_keyboard(
                form=form, 
                fac=fac, 
                group=group, 
                date_page=date_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def week_select_page(self, id: int) -> None:
        db.change_stage(user_id=id, stage=self.sn.WEEK_SELECT)
        week_page = db.get_week_page(user_id=id)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = db.get_group(user_id=id)
        subgroup = db.get_subgroup(user_id=id)
        quality = db.get_quality(user_id=id)
        mode = db.get_mode(user_id=id)
        text = 'Выберите неделю:'
        keyboard = stage_week_keyboard(
                week_page=week_page, 
                form=form, 
                fac=fac, 
                group=group, 
                subgroup=subgroup, 
                quality=quality, 
                mode=mode
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def settings_week_page(self, id: int, edit: str|None = None) -> None:
        """ edit = None -> переход на страницу с настройками
        edit = 'mode' -> изменение цветовой схемы
        edit = 'quality' -> изменение качество изображений"""
        if edit == None:
            text = 'Выберите:'
            db.change_stage(user_id=id, stage=self.sn.SETTINGS_WEEK)
        elif edit == 'mode':
            text = 'Изменена цветовая схема'
            db.change_mode(user_id=id)
        elif edit == 'quality':
            text = 'Изменено качество изображений'
            db.change_quality(user_id=id)
        else:
            return
        mode = db.get_mode(user_id=id)
        quality = db.get_quality(user_id=id)
        keyboard = stage_settings_week_keyboard(mode=mode, 
            quality=quality)
        self.s.sender(id=id, text=text, keyboard=keyboard)
