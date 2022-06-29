from Lib.BotDB_Func import BotDB_Func
from Lib.keyboards import *
from config import db_path, data_folder

db = BotDB_Func(db_path=db_path)

class Pages:
    def __init__(self, sender):
        self.s = sender

    def start_page(self):
        pass


    def home_page(self, id: int, null:bool|None=None):
        db.change_stage(user_id=id, stage=100)
        if null is not None:
            db.null_user(user_id=id)
        stage = 100
        subgroup = db.get_subgroup(user_id=id)
        text = "Выберите: "
        keyboard = stage_home_keyboard(stage=stage, subgroup=subgroup)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def other_page(self, id: int):
        db.change_stage(user_id=id, stage=101)
        text = 'Выберите: '
        can_get_teachers = False
        if 'teachers' in db.get_passwords(user_id=id):
            can_get_teachers = True
        keyboard = stage_other_keyboard(can_get_teachers=can_get_teachers)
        self.s.sender(id=id, text=text, keyboard=keyboard)
        

    def passwords_page(self, id: int, event):
        db.change_stage(user_id=id, stage=102)
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
            text = '🔵Для добавления пароля, находясь в данной вкладке '\
                    '("Пароли"), напишите боту сообщение с придуманным '\
                    'кодовым словом. (Вводить без пробелов)\n' \
                    'После этого у Вас будет возможность '\
                    'выбрать тип пароля:\n'\
                    '➡Открытая -> делать рассылку могут все '\
                    'пользователи, которые ввели пароль\n'\
                    '➡Приватная -> делать рассылку может только '\
                    'создатель пароля\n\n'\
                    '🔵Для удаления пароля, находясь в данной '\
                    'вкладке ("Пароли"), напишите боту сообщение: '\
                    '"del кодовое слово"\n'\
                    'Пример: del 123\n(у вас удалится пароль 123)\n\n'\
                    '🔵Список Ваших паролей можно найти при нажатии '\
                    'кнопки "Мои пароли". \n\n' \
                    '❕Для рассылки сообщений всем,у кого введён '\
                    'такой же пароль, перейдите на любую другую страницу '\
                    'бота и введите "пароль сообщение".\n' \
                    'Пример: 123 Всем привет!\n' \
                    '(всем пользователям с введенным кодовым словом '\
                    '123 отправится сообщение "Всем привет!" )'
            self.s.sender(id=id, text=text)
        text = 'Введите пароль:'
        keyboard = stage_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def setting_password_page(self, id: int):
        text = f'Выберите параметр приватности рассылки:\n'\
                'Приватная -> делать рассылку может только '\
                'создатель\n'\
                'Открытая -> делать рассылку могут все '\
                'пользователи, которые ввели пароль'
        db.change_stage(user_id=id, stage=103)
        keyboard = stage_setting_passwords_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def mail_page(self, id: int):
        db.change_stage(user_id=id, stage=104)
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
            db.change_stage(user_id=id, stage=1)
            db.null_schedule(user_id=id)
        text = "Выберите одну из форм обучения:"
        keyboard = stage_form_keyboard(data_folder=data_folder)
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def fac_page(self, id: int, msg: str):
        forms = get_forms(data_folder=data_folder)
        for form in forms:
            if form.lower() == msg:
                db.change_stage(user_id=id, stage=2)
                db.change_form(user_id=id, form=form)
                text = 'Выберите один из факультетов:'
                keyboard = stage_fac_keyboard(
                        data_folder=data_folder, 
                        form=form
                        )
                self.s.sender(id=id, text=text, keyboard=keyboard)

    def group_select_page(self, id: int, msg: None|str = None, 
            update_stage: bool|None = None):
        fac = ''
        if msg is not None:
            form = db.get_form(user_id=id)
            group_page = db.get_group_page(user_id=id)
            facs = get_facs(data_folder=data_folder, form=form)
            for fac in facs:
                if fac.lower() == msg:
                    db.change_fac(user_id=id, fac=fac)
                    db.change_stage(user_id=id, stage=3)
                    break
        else:
            if update_stage is not None:
                db.change_stage(user_id=id, stage=3)
            db.del_group(user_id=id)
            db.del_subgroup(user_id=id)
            form = db.get_form(user_id=id)
            fac = db.get_fac(user_id=id)
            group_page = db.get_group_page(user_id=id)
        text = f'Выберите одну из групп:\nПоказана страница {group_page}'
        keyboard = stage_group_keyboard(
                data_folder=data_folder, 
                form=form, 
                fac=fac, 
                group_page=group_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def session_group_select_page(self, id: int, update_stage:bool|None = None):
        if update_stage is not None:
            db.change_stage(user_id=id, stage=3.5)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        session_group_page = db.get_session_group_page(user_id=id)
        text = f'Выберите одну из групп:\nПоказана страница {session_group_page}'
        keyboard = stage_session_group_keyboard(
                data_folder=data_folder, 
                form=form, 
                fac=fac, 
                session_group_page=session_group_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def subgroup_page(self, id: int, session:None|bool=None, msg:None|str=None):
        group = ''
        if msg is not None:
            form = db.get_form(user_id=id)
            fac = db.get_fac(user_id=id)
            if session == True:
                groups = get_session_groups(data_folder=data_folder, form=form, fac=fac)
            else:
                groups = get_groups(data_folder=data_folder, form=form, fac=fac)
            for group in groups:
                if group.lower() == msg:
                    db.change_stage(user_id=id, stage=4)
                    db.change_group(user_id=id, group=group)
                    break
        else:
            db.change_stage(user_id=id, stage=4)
            db.del_subgroup(user_id=id)
            form = db.get_form(user_id=id)
            fac = db.get_fac(user_id=id)
            group = db.get_group(user_id=id)
        text = 'Выберите подгруппу:'
        keyboard = stage_subgroup_keyboard(
                data_folder=data_folder, 
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
                    data_folder=data_folder, 
                    form=form, 
                    fac=fac, 
                    group=group
                    )
            for subgroup in range(1, all_subgroups + 1):
                if str(subgroup).lower() == msg:
                    db.change_subgroup(user_id=id, subgroup=str(subgroup))
        db.change_stage(user_id=id, stage=5)
        text = 'Выберите: '
        keyboard = stage_schedule_type_keyboard()
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def date_select_page(self, id: int, update:bool|None=None):
        db.change_stage(user_id=id, stage=6)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = db.get_group(user_id=id)
        date_page = db.get_date_page(user_id=id)
        if update is not None:
            text = 'Даты обновлены'
        else:
            text = f'Выберите дату:\nПоказана страница {date_page}'
        keyboard = stage_date_keyboard(
                data_folder=data_folder, 
                form=form, 
                fac=fac, 
                group=group, 
                date_page=date_page
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def week_select_page(self, id: int):
        db.change_stage(user_id=id, stage=7)
        week_page = db.get_week_page(user_id=id)
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = db.get_group(user_id=id)
        subgroup = db.get_subgroup(user_id=id)
        quality = db.get_quality(user_id=id)
        mode = db.get_mode(user_id=id)
        text = 'Выберите неделю:'
        keyboard = stage_week_keyboard(
                data_folder=data_folder, 
                week_page=week_page, 
                form=form, 
                fac=fac, 
                group=group, 
                subgroup=subgroup, 
                quality=quality, 
                mode=mode
                )
        self.s.sender(id=id, text=text, keyboard=keyboard)


    def settings_week_page(self, id: int):
        db.change_stage(user_id=id, stage=8)
        text = 'Выберите:'
        mode = db.get_mode(user_id=id)
        quality = db.get_quality(user_id=id)
        keyboard = stage_settings_week_keyboard(mode=mode, quality=quality)
        self.s.sender(id=id, text=text, keyboard=keyboard)
