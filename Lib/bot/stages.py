from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.keyboards import *
from Lib.bot.stages_names import Stages_names
from Lib.bot.output_texts import (passwords_info_str, 
                                settings_password_str, start_message_str)
from config import db_path

db = BotDB_Func(db_path=db_path)

class Pages:
    def __init__(self, sender):
        self.s = sender
        self.sn = Stages_names()
    

    def reset_page(self, user_id: int):
        text = f"Кнопки сброшены\nОбновление!\n[ Информацию об обновлении "\
            f"искать на странице сообщества ]\nНажмите кнопку 'Начать'"
        keyboard = stage_start_keyboard()
        self.s.sender(id=user_id, text=text, keyboard=keyboard)


    def start_page(self, id:int):
        db.start(user_id=id)
        text = start_message_str()
        self.s.sender(id=id, text=text)
        Pages.home_page(self, id=id, null_user=True)


    def home_page(self, id: int, null_user:bool|None=None):
        db.change_stage(user_id=id, stage=self.sn.HOME)
        if null_user is not None:
            db.null_user(user_id=id)
        subgroup = db.get_subgroup(user_id=id)
        text = "Выберите: "
        keyboard = stage_home_keyboard(subgroup=subgroup)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def other_page(self, id: int):
        db.change_stage(user_id=id, stage=self.sn.OTHER)
        text = 'Выберите: '
        can_get_teachers = False
        if 'teachers' in db.get_passwords(user_id=id):
            can_get_teachers = True
        keyboard = stage_other_keyboard(can_get_teachers=can_get_teachers)
        self.s.sender(id=id, text=text, keyboard=keyboard)
        

    def passwords_page(self, id: int, event):
        db.change_stage(user_id=id, stage=self.sn.PASSWORDS)
        if 'callback' in event.button_actions:
            text = 'Что такое код-пароль?'
            settings = dict(inline=True)
            inline_keyboard = VkKeyboard(**settings)
            inline_keyboard.add_callback_button(
                    label='Узнать', 
                    color=VkKeyboardColor.POSITIVE, 
                    payload={'type': 'what_is_password'}
                    )
            self.s.sender(id=id, text=text, inline_keyboard=inline_keyboard)
        else:
            text = passwords_info_str() 
            self.s.sender(id=id, text=text)
        text = 'Введите пароль:'
        keyboard = stage_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def setting_password_page(self, id: int):
        db.change_stage(user_id=id, stage=self.sn.SETTING_PASSWORDS)
        text = settings_password_str()
        keyboard = stage_setting_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def mail_page(self, id: int):
        db.change_stage(user_id=id, stage=self.sn.MAIL)
        daily_mail = db.get_daily_mail(user_id=id)
        weekly_mail = db.get_weekly_mail(user_id=id)
        text = 'Включите/выключите рассылку расписания:'
        keyboard = stage_mail_keyboard(
                daily_mail=daily_mail, 
                weekly_mail=weekly_mail
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def form_page(self, id: int, update_forms: bool|None = None):
        if update_forms is None:
            db.change_stage(user_id=id, stage=self.sn.FORM)
            db.null_schedule(user_id=id)
        text = "Выберите одну из форм обучения:"
        keyboard = stage_form_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def fac_page(self, id: int, msg: str):
        forms = get_forms()
        for form in forms:
            if form.lower() == msg:
                db.change_stage(user_id=id, stage=self.sn.FAC)
                db.change_form(user_id=id, form=form)
                text = 'Выберите один из факультетов:'
                keyboard = stage_fac_keyboard(form=form)
                self.s.sender(id=id, text=text, keyboard=keyboard)

    def group_select_page(self, id: int, msg: None|str = None, 
            update_stage: bool|None = None):
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


    def session_group_select_page(self, id: int, update_stage:bool|None = None):
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


    def subgroup_page(self, id: int, session:None|bool=None, msg:None|str=None):
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
            db.change_stage(user_id=id, stage=self.sn.SUBGROUP)
            db.del_subgroup(user_id=id)
            group = db.get_group(user_id=id)
        text = 'Выберите подгруппу:'
        keyboard = stage_subgroup_keyboard(
                form=form, 
                fac=fac, 
                group=group
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def schedule_type_page(self, id: int, msg: str|None = None):
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
        text = 'Выберите: '
        keyboard = stage_schedule_type_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def date_select_page(self, id: int, update:bool|None=None):
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


    def week_select_page(self, id: int):
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


    def settings_week_page(self, id: int, edit: str | None = None):
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
        keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
        self.s.sender(id=id, text=text, keyboard=keyboard)