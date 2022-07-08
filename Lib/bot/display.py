import json
from Lib.bot.output_texts import schedule_str, teachers_info_str
from Lib.bot.inline_keyboards import bot_info
from Lib.bot.getter import get_schedule_path


class Display:
    def __init__(self, db, s):
        self.db = db
        self.s = s

    def schedule_display(self, id: int, msg: str):
        """ Отправляет сообщение с расписанием по дате """
        form = self.db.get_form(user_id=id)
        fac = self.db.get_fac(user_id=id)
        group = self.db.get_group(user_id=id)
        subgroup = self.db.get_subgroup(user_id=id)
        path = get_schedule_path(form=form, fac=fac, group=group)
        with open(path) as f:
            data = json.load(f)
        for date in data:
            if date['date'] == msg.split(' ')[1]:
                try:
                    if date['date'] == msg.split(' ')[1]:
                        if date['lessons'][0]['day_of_week'] in msg:
                            text = schedule_str(
                                    data=date, 
                                    subgroup=subgroup, 
                                    date=date['date'])
                            self.s.sender(id=id, text=text)
                except:
                    pass


    def bot_info_display(self, button_actions, id: int):
        """ Отправляет сообщение с информацией о боте """

        text = 'Данный бот дублирует информацию о расписании с '\
            'официального сайта МГТУ ГА ' \
            '( обновление информации в боте '\
            'происходит каждую среду )\n' \
            'Вся информация собрана из открытых источников\n\n'\

        if 'callback' in button_actions:
            text += f'Вопросы и предложения писать разработчику '\
                f'или в обсуждении:'
            inline_keyboard = bot_info()
            self.s.sender(id=id, text=text, inline_keyboard=inline_keyboard)
        else:
            text += 'Вопросы и предложения писать '\
                'разработчику - @id478270913 или в '\
                'обсуждении https://vk.com/topic-210110232_48270692'
            self.s.sender(id=id, text=text)


    def teachers_display(self, id: int):
        teachers_info = teachers_info_str(db=self.db, id=id)
        self.s.sender(id=id, text=teachers_info)


    def passwords_info_display(self, id: int):
        user_passwords = self.db.get_passwords(user_id=id)
        if not len(user_passwords) == 0:
            text = ''
            for password in user_passwords:
                creator = self.db.get_creator(password=password)
                privacy = self.db.get_privacy(password=password)
                text += f'✅Пароль: {password}\nСоздатель: @id{creator}\n'\
                        f'Приватность: {"+" if privacy == 1 else "-"}\n\n'
        else:
            text = 'Нет сохраненных паролей'
        self.s.sender(id=id, text=text)
