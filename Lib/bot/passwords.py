from Lib.bot.bot_return import Returns, fast_return
from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.stages import Pages
# from config import db_path

db = BotDB_Func()
pages = Pages()


class Passwords:
    def del_password(self, message: str, user_id: int) -> Returns:
        entered_password = message.removeprefix('del')
        entered_password = entered_password.removeprefix('Del')
        entered_password = entered_password.strip()
        text = ''
        for pwd in db.get_passwords(user_id=user_id):
            if pwd == entered_password:
                success = db.del_password(user_id=user_id, 
                    password=pwd)
                if success:
                    text = f'Пароль #{entered_password} удален'
        if text == '':
            text = 'Пароль не найден'
        return fast_return(user_id=user_id, text=text)


    def add_password(self, message: str, user_id: int) -> Returns:
        result = Returns()
        password = message
        if 'пароли' not in password.lower():
            text, key = db.add_password(user_id=user_id, 
                password=password)
            result.add_return(user_id=user_id, text=text)
            if key == 1 | True:
                """ Отправляем сообщение всем пользователям 
                    с password=password """
                text = f'Пользователь @id{user_id} ввел '\
                    f'пароль #{password}'
                for user in db.get_all_users_with_pass(
                        password=password):
                    result.add_return(user_id=user, text=text)
                if db.get_privacy(password=password) == None:
                    """ Переход на stage 103 """
                    result.returns += (
                        pages.setting_password_page(
                        id=user_id).returns)
        return result
