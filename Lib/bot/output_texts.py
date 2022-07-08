import os
import json

def schedule_str(data: dict, subgroup: str, date: str) -> str:
    """ Выводит str расписания """
    text = 'Ошибка'
    times_of_lesson = ['8:30 - 10:00', '10:10 - 11:40', '12:40 - 14:10', 
            '14:20 - 15:50', '16:20 - 17:50', '18:00 - 19:30']

    if data['date'] == date:
        lessons_list = [item for item in data['lessons']]
        new_list = []
        for _ in range(1, len(lessons_list) + 1):
            min_num = {
                'num': 1000
            }
            min_index = 100
            for entry in enumerate(lessons_list):
                if int(entry[1]['num']) < int(min_num['num']):
                    min_num = entry[1]
                    min_index = int(entry[0])
            new_list.append(min_num)
            lessons_list.pop(min_index)
        text = f"{data['date']}  "\
                f"{data['lessons'][0]['day_of_week'].capitalize()}\n\n"
        for entry in new_list:
            if entry['subgroup'] == subgroup or entry['subgroup'] == "":
                text += f'{entry["num"]} - '\
                        f'({times_of_lesson[int(entry["num"]) - 1]})\n'\
                        f'{entry["lesson_name"]} - {entry["type_of_lesson"]}'\
                        f'\n{entry["name"]}\n{entry["room"]}\n\n'
    return text.strip()

def teachers_info_str(db, id: int) -> str:
    """ Выводит информацию о преподавателях из файла teachers.json 
    в формате str"""
    if 'teachers' in db.get_passwords(user_id=id):
        path = f'{os.getcwd()}\\users_data\\teachers.json'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as teachers:
                list_of_teachers = json.load(teachers)
            text = ""
            for teacher in list_of_teachers:
                text += f'Имя: {teacher["name"]}\n'\
                        f'Телефон: {teacher["phone"]}\n'\
                        f'Почта: {teacher["mail"]}\n\n'
        else:
            text = 'Информация о преподавателях не найдена :c'
    else: 
        text = 'У вас нет доступа для получения '\
                'информации о преподавателях'
    return text


def passwords_info_str() -> str:
    text = '🔵Для добавления пароля, находясь в данной вкладке '\
        '("Пароли"), напишите боту сообщение с придуманным '\
        'кодовым словом. (Вводить без пробелов)\n' \
        'После этого у Вас будет возможность выбрать тип пароля:\n'\
        '➡Открытая -> делать рассылку могут все '\
        'пользователи, которые ввели пароль\n'\
        '➡Приватная -> делать рассылку может только создатель пароля\n\n'\
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
    return text


def settings_password_str() -> str:
    text = f'Выберите параметр приватности рассылки:\n'\
            'Приватная -> делать рассылку может только '\
            'создатель\n'\
            'Открытая -> делать рассылку могут все '\
            'пользователи, которые ввели пароль'
    return text


def start_message_str() -> str:
    text = f'Привет😉\nДанный бот дублирует информацию о расписании '\
            'с официального сайта МГТУ ГА '\
            '( обновление информации в боте происходит каждую среду )'\
            f'\nВся информация собрана из открытых источников\n\n'
    return text
