import json
from typing import List

from Lib.bot.output_texts import error_return_str
from Lib.bot.output_texts import schedule_str
from Lib.bot.output_texts import teachers_info_str 

from Lib.bot.inline_keyboards import bot_info
from Lib.bot.keyboards import stage_preset_keyboard
from Lib.bot.bot_getter import get_schedule_path
from Lib.bot.event_hint import Event_hint
from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.bot_return import Returns, error_return
# from config import db_path


db = BotDB_Func()


class Display:

    def schedule_display(self, id: int, msg: str) -> Returns:
        """ Отправляет сообщение с расписанием по дате """
        try:
            msg.split(' ')[1]
        except:
            return error_return(user_id=id)
        result = Returns()
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
                                group=group,
                                subgroup=subgroup, 
                                date=date['date'])
                            result.add_return(user_id=id, text=text)
                            return result
                except:
                    pass
        text = error_return_str()
        result.add_return(user_id=id, text=text)
        return result


    def bot_info_display(self, button_actions: List[str], id: int) -> Returns:
        """ Отправляет сообщение с информацией о боте """

        result = Returns()
        text = 'Данный бот дублирует информацию о расписании с '\
            'официального сайта МГТУ ГА ' \
            '( обновление информации в боте '\
            'происходит каждую среду )\n' \
            'Вся информация собрана из открытых источников\n\n'\

        if 'callback' in button_actions:
            text += f'Вопросы и предложения писать разработчику '\
                f'или в обсуждении:'
            inline_keyboard = bot_info()
            result.add_return(user_id=id, text=text, 
                inline_buttons=inline_keyboard)
        else:
            text += 'Вопросы и предложения писать '\
                'разработчику - @id478270913 или в '\
                'обсуждении https://vk.com/topic-210110232_48270692'
            result.add_return(user_id=id, text=text)
        return result


    def teachers_display(self, id: int) -> Returns:
        """ Отправляет информацию о преподавателях """
        result = Returns()
        teachers_info = teachers_info_str(id=id)
        result.add_return(user_id=id, text=teachers_info)
        return result


    def passwords_info_display(self, id: int) -> Returns:
        """ Отправляет информацию о сохраненных паролях пользователя """
        result = Returns()
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
        result.add_return(user_id=id, text=text)
        return result

    def presets_display(self, user_id, event: Event_hint) -> Returns:
        """ Изменяет / удаляет пресет пользователя """
        result = Returns()
        user_presets = db.get_all_user_presets(user_id=user_id)
        if ('].' in event.msg and 
            int(event.msg[0]) in user_presets and 
            len(user_presets) > 1):
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
                    result.add_return(user_id=user_id, text=warning_text)
                elif chosen_preset > int(event.msg[0]):
                    chosen_preset -= 1
                    db.change_preset(user_id=user_id, preset=chosen_preset)
                keyboard = stage_preset_keyboard(presets=presets, 
                    chosen_preset=chosen_preset, on_delete=True)
            result.add_return(user_id=user_id, text=text, buttons=keyboard)
        elif len(user_presets) <= 1:
            text = 'Нельзя удалить последний пресет!'
            result.add_return(user_id=user_id, text=text)
        else:
            result.add_return(user_id=user_id, text=error_return_str())
        return result
