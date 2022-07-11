from Lib.bot.BotDataBase import BotDB 
from typing import NamedTuple

class Error_handler(NamedTuple):
    error: str | None
    key: int

def _wrapper(key: int) -> Error_handler:
    errors = {
            "1": "Пароль успешно добавлен",
            "True": "Пароль успешно добавлен",
            "0": "Пароль должен состоять из 1 слова",
            "False": "Ошибка выполнения",
            "101": f"Пароль уже создан, но не настроен\n"\
                    "Попробуйте в другой раз",
            "102": "Этот пароль уже добавлен",
            "200": "Пользователь уже добавлен",
            "201": "Пользователь добавлен в базу",
            }
    try:
        error = errors.get(f'{key}')
    except:
        error = 'Failed'
    return Error_handler(error=error, key=key)


class BotDB_Func:
    def __init__(self, db_path):
        self.db_path = db_path

    def start(self, user_id: int) -> int:
        """ Проверяем, есть ли пользователь в базе
        Если нет, то добавляем в базу"""
        with BotDB(self.db_path) as db:
            if not db.user_exists(user_id=user_id):
                db.add_user(user_id=user_id)
                return 201
            return 200

    def get_users(self) -> list:
        """ Получаем список всех пользователей """
        with BotDB(self.db_path) as db:
            users = db.get_users()
            return users

    def null_user(self, user_id: int):
        """ Сбрасываем все данные пользователя """
        with BotDB(self.db_path) as db:
            db.null_user(user_id=user_id)

    def null_schedule(self, user_id: int):
        """ Сбрасываем расписание пользователя """
        with BotDB(self.db_path) as db:
            db.null_schedule(user_id=user_id)

    def get_stage(self, user_id: int) -> str:
        """ Получаем stage пользователя """
        with BotDB(self.db_path) as db:
            stage = db.get_stage(user_id=user_id)
            return stage

    def change_stage(self, user_id: int, stage: str):
        """ Меняем stage пользователя """
        with BotDB(self.db_path) as db:
            db.change_stage(user_id=user_id, stage=stage)

    def get_form(self, user_id: int) -> str:
        """Получаем form пользователя"""
        with BotDB(self.db_path) as db:
            form = db.get_form(user_id=user_id)
            return form

    def change_form(self, user_id: int, form: str):
        """Меняем form пользователя"""
        with BotDB(self.db_path) as db:
            db.change_form(user_id=user_id, form=form)

    def del_form(self, user_id: int):
        """ Удаляем form пользователя """
        with BotDB(self.db_path) as db:
            db.del_form(user_id=user_id)

    def get_fac(self, user_id: int) -> str:
        """ Получаем fac пользователя """
        with BotDB(self.db_path) as db:
            fac = db.get_fac(user_id=user_id)
            return fac

    def change_fac(self, user_id: int, fac: str):
        """ Меняем fac пользователя """
        with BotDB(self.db_path) as db:
            db.change_fac(user_id=user_id, fac=fac)

    def del_fac(self, user_id: int):
        """ Удаляем fac пользователя """
        with BotDB(self.db_path) as db:
            db.del_fac(user_id=user_id)

    def get_group_page(self, user_id: int) -> int:
        """ Получаем group_page пользователя """
        with BotDB(self.db_path) as db:
            group_page = db.get_group_page(user_id=user_id)
            return group_page

    def change_group_page(self, user_id: int, group_page: int):
        """ Меняем group_page пользователя """
        with BotDB(self.db_path) as db:
            db.change_group_page(user_id=user_id, group_page=group_page)

    def get_session_group_page(self, user_id: int) -> int:
        """ Получаем session_group_page пользователя """
        with BotDB(self.db_path) as db:
            session_group_page = db.get_session_group_page(user_id=user_id)
            return session_group_page

    def change_session_group_page(self, user_id: int, session_group_page: int):
        """ Меняем session_group_page пользователя """
        with BotDB(self.db_path) as db:
            db.change_session_group_page(
                    user_id=user_id, 
                    session_group_page=session_group_page
                    )

    def get_group(self, user_id: int) -> str:
        """ Получаем group пользователя """
        with BotDB(self.db_path) as db:
            group = db.get_group(user_id=user_id)
            return group

    def change_group(self, user_id: int, group: str):
        """ Меняем group пользователя """
        with BotDB(self.db_path) as db:
            db.change_group(user_id=user_id, group=group)

    def del_group(self, user_id: int):
        """ Удаляем group пользователя """
        with BotDB(self.db_path) as db:
            db.del_group(user_id=user_id)

    def get_subgroup(self, user_id: int) -> str:
        """ Получаем subgroup пользователя """
        with BotDB(self.db_path) as db:
            subgroup = db.get_subgroup(user_id=user_id)
            return subgroup

    def change_subgroup(self, user_id: int, subgroup: str):
        """ Меняем subgroup пользователя """
        with BotDB(self.db_path) as db:
            db.change_subgroup(user_id=user_id, subgroup=subgroup)

    def del_subgroup(self, user_id: int):
        """ Удаляем subgroup пользователя """
        with BotDB(self.db_path) as db:
            db.del_subgroup(user_id=user_id)

    def get_quality(self, user_id: int) -> int:
        """ Получаем quality пользователя """
        with BotDB(self.db_path) as db:
            quality = db.get_quality(user_id=user_id)
            return quality

    def change_quality(self, user_id: int):
        """ Меняем quality пользователя """
        with BotDB(self.db_path) as db:
            db.change_quality(user_id=user_id)

    def get_mode(self, user_id: int) -> str:
        """ Получаем mode пользователя """
        with BotDB(self.db_path) as db:
            mode = db.get_mode(user_id=user_id)
            return mode

    def change_mode(self, user_id: int):
        """ Меняем mode пользователя """
        with BotDB(self.db_path) as db:
            db.change_mode(user_id=user_id)

    def get_week_page(self, user_id: int) -> int:
        """ Получаем week_page пользователя """
        with BotDB(self.db_path) as db:
            week_page = db.get_week_page(user_id=user_id)
            return week_page

    def change_week_page(self, user_id: int, week_page: int):
        """ Меняем week_page пользователя """
        with BotDB(self.db_path) as db:
            db.change_week_page(user_id=user_id, week_page=week_page)

    def get_date_page(self, user_id: int) -> int:
        """ Получаем date_page пользователя """
        with BotDB(self.db_path) as db:
            date_page = db.get_date_page(user_id=user_id)
            return date_page

    def change_date_page(self, user_id: int, date_page: int):
        """ Меняем date_page пользователя """
        with BotDB(self.db_path) as db:
            db.change_date_page(user_id=user_id, date_page=date_page)

    def get_daily_mail(self, user_id: int) -> int:
        """ Получаем daily_mail пользователя """
        with BotDB(self.db_path) as db:
            daily_mail = db.get_daily_mail(user_id=user_id)
            return daily_mail

    def change_daily_mail(self, user_id: int, daily_mail: int):
        """ Меняем daily_mail пользователя """
        with BotDB(self.db_path) as db:
            db.change_daily_mail(user_id=user_id, daily_mail=daily_mail)

    def get_all_daily_mail(self) -> list:
        """ Получаем всех пользователей с daily_mail = 1 """
        with BotDB(self.db_path) as db:
            users_id = db.get_all_daily_mail()
            return users_id

    def get_weekly_mail(self, user_id: int) -> int:
        """ Получаем weekly_mail пользователя """
        with BotDB(self.db_path) as db:
            weekly_mail = db.get_weekly_mail(user_id=user_id)
            return weekly_mail

    def change_weekly_mail(self, user_id: int, weekly_mail: int):
        """ Меняем weekly_mail пользователя """
        with BotDB(self.db_path) as db:
            db.change_weekly_mail(user_id=user_id, weekly_mail=weekly_mail)

    def get_all_weekly_mail(self) -> list:
        """ Получаем всех пользователей с weekly_mail = 1 """
        with BotDB(self.db_path) as db:
            users_id = db.get_all_weekly_mail()
            return users_id

    def get_passwords(self, user_id: int) -> list:
        """ Получаем passwords пользователя """
        with BotDB(self.db_path) as db:
            passwords = db.get_passwords(user_id=user_id)
            return passwords

    def _set_creator(self, creator_id: int, password: str) -> None:
        """ Меняем создателя пароля """
        with BotDB(self.db_path) as db:
            db._set_creator(creator_id=creator_id, password=password)

    def get_creator(self, password: str) -> int | None:
        """ Получаем user_id создателя пароля """
        with BotDB(self.db_path) as db:
            creator = db.get_creator(password=password)
            return creator

    def get_privacy(self, password: str) -> int | None:
        """ Получаем privacy пароля """
        with BotDB(self.db_path) as db:
            privacy = db.get_privacy(password=password)
            return privacy

    def add_password(self, user_id: int, password: str) -> Error_handler:
        """ Добавляем password пользователю """
        with BotDB(self.db_path) as db:
            success = db.add_password(user_id=user_id, password=password)
            text, key = _wrapper(key=success)
            return Error_handler(error=text, key=key)

    def set_privacy(self, user_id: int, privacy: int) -> str:
        with BotDB(self.db_path) as db:
            password = db.set_privacy(user_id=user_id, privacy=privacy)
            return password
    
    def del_password(self, user_id: int, password: str) -> bool:
        """ Удаляем password пользователю """
        with BotDB(self.db_path) as db:
            success = db.del_password(user_id=user_id, password=password)
            return success

    def get_all_users_with_pass(self, password: str) -> list:
        """ Получаем всех пользователей, у которых есть password """
        with BotDB(self.db_path) as db:
            users_id = db.get_all_passwords(password=password) 
            return users_id
