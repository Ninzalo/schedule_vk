import json
from Lib.bot.output_texts import schedule_str, teachers_info_str
from Lib.bot.inline_keyboards import bot_info
from Lib.bot.keyboards import stage_preset_keyboard
from Lib.bot.bot_getter import get_schedule_path
from Lib.bot.event_hint import Event_hint
from Lib.bot.BotDB_Func import BotDB_Func
from config import db_path


db = BotDB_Func(db_path=db_path)


class Display:
    def __init__(self, s):
        self.s = s

    def schedule_display(self, id: int, msg: str) -> None:
        """ Отправляет сообщение с расписанием по дате """
        form = db.get_form(user_id=id)
        fac = db.get_fac(user_id=id)
        group = db.get_group(user_id=id)
        subgroup = db.get_subgroup(user_id=id)
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


    def bot_info_display(self, button_actions, id: int) -> None:
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


    def teachers_display(self, id: int) -> None:
        """ Отправляет информацию о преподавателях """
        teachers_info = teachers_info_str(id=id)
        self.s.sender(id=id, text=teachers_info)


    def passwords_info_display(self, id: int) -> None:
        """ Отправляет информацию о сохраненных паролях пользователя """
        user_passwords = db.get_passwords(user_id=id)
        if not len(user_passwords) == 0:
            text = ''
            for password in user_passwords:
                creator = db.get_creator(password=password)
                privacy = db.get_privacy(password=password)
                text += f'✅Пароль: {password}\nСоздатель: @id{creator}\n'\
                        f'Приватность: {"+" if privacy == 1 else "-"}\n\n'
        else:
            text = 'Нет сохраненных паролей'
        self.s.sender(id=id, text=text)

    def presets_display(self, user_id, event: Event_hint) -> None:
        """ Изменяет / удаляет пресет пользователя """
        user_presets = db.get_all_user_presets(user_id=user_id)
        if ('].' in event.msg and int(event.msg[0]) in user_presets
                and len(user_presets) > 1):
            if db.get_on_delete(user_id=user_id) == 0:
                text = f'Выбран пресет {event.message}'
                db.change_preset(user_id=user_id, preset=int(event.msg[0]))
                presets = db.get_user_preset_data(user_id=user_id)
                chosen_preset = db.get_preset(user_id=user_id)
                keyboard = stage_preset_keyboard(presets=presets, 
                        chosen_preset=chosen_preset)
            else:
                text = f'Пресет {event.message} удален'
                db.del_preset_by_num(user_id=user_id, 
                        preset_num=int(event.msg[0]))
                db.update_preset_num(user_id=user_id, 
                        deleted_preset_num=int(event.msg[0]))
                presets = db.get_user_preset_data(user_id=user_id)
                chosen_preset = db.get_preset(user_id=user_id)
                if chosen_preset == int(event.msg[0]):
                    chosen_preset = 1
                    db.change_preset(user_id=user_id, preset=chosen_preset)
                    warning_text = f'Выбранный пресет удален\n'\
                            f'Автоматическое переключение на пресет [1]'
                    self.s.sender(id=user_id, text=warning_text)
                elif chosen_preset > int(event.msg[0]):
                    chosen_preset -= 1
                    db.change_preset(user_id=user_id, preset=chosen_preset)
                keyboard = stage_preset_keyboard(presets=presets, 
                        chosen_preset=chosen_preset, on_delete=True)
            self.s.sender(id=user_id, text=text, keyboard=keyboard)
        elif len(user_presets) <= 1:
            text = 'Нельзя удалить последний пресет!'
            self.s.sender(id=user_id, text=text)
