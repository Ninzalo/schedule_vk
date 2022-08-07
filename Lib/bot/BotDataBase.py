import sqlite3
from typing import Tuple, List, Union, Optional


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def user_exists(self, user_id: int) -> bool:
        """Проверяем, есть ли юзер в базе"""
        sql = """SELECT user_id FROM users_info WHERE user_id = ?"""
        result = self.cursor.execute(sql, (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id: int) -> int:
        """Достаем id юзера в базе по его user_id"""
        sql = """ SELECT id FROM users WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id: int) -> None:
        """Добавляем юзера в базу"""
        sql = """ INSERT INTO users_info (user_id) VALUES (?) """
        self.cursor.execute(sql, (user_id,))
        sql = """ INSERT INTO users (user_id) VALUES (?) """
        self.cursor.execute(sql, (user_id,))
        return self.conn.commit()

    def get_users(self) -> list:
        """ Достаем user_id всех пользователей """
        sql = """ SELECT user_id FROM users_info """
        result = self.cursor.execute(sql)
        result = [int(item[0]) for item in result.fetchall()]
        return result

    def null_user(self, user_id: int) -> None:
        """ Выставляем стандартное значение stage и всех параметров """
        sql = """ DELETE FROM users WHERE user_id = ? AND preset_num > 1 """
        self.cursor.execute(sql, (user_id,))
        sql = """ UPDATE users 
        SET group_page=1, session_group_page=1, week_page=0, 
        date_page=1, form=null, fac=null, subgroup=null, group_name=null
        WHERE user_id=?"""
        self.cursor.execute(sql, (user_id,))
        sql = """ UPDATE users_info 
        SET on_stage='home', chosen_preset = 1, 
        new_group = 0, on_delete_page = 0        
        WHERE user_id = ? """
        self.cursor.execute(sql, (user_id,))
        return self.conn.commit()

    def null_schedule(self, user_id: int) -> None:
        """ Выставляем стандартное значение всех параметров расписания """
        sql = """ UPDATE users
        SET form=null, fac=null, group_page=1, group_name=null, subgroup=null, 
        week_page=0, date_page=1, session_group_page=1
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def add_new_preset(self, user_id: int) -> None:
        """ Добавляем новый пресет пользователю """
        sql = """ INSERT INTO users (user_id, preset_num) VALUES (?, ?) """
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_preset(self, user_id: int) -> int:
        """ Получаем chosen_preset пользователя """
        sql = """ SELECT chosen_preset FROM users_info WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        return result.fetchone()[0]

    def change_preset(self, user_id: int, preset: int) -> None:
        """ Изменяем chosen_preset пользователя """
        sql = """UPDATE users_info SET chosen_preset = ? WHERE user_id = ?"""
        self.cursor.execute(sql, (preset, user_id))
        return self.conn.commit()

    def get_all_user_presets(self, user_id: int) -> list:
        """ Получаем все preset_num пользователя """
        sql = """ SELECT preset_num FROM users WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        result_list = []
        for item in result.fetchall():
            result_list.append(int(item[0]))
        return result_list

    def get_user_preset_data(self, user_id: int) -> List[Tuple[int, str, str, str, str]]:
        """ Получаем данные по всем пресетам пользователя """
        sql = """ SELECT preset_num, form, fac, group_name, subgroup FROM users 
        WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        result = result.fetchall()
        return result

    def add_new_group(self, user_id: int) -> bool:
        """Проверяем, добавляем ли новую группу """
        sql = """SELECT new_group FROM users_info WHERE user_id = ?"""
        result = self.cursor.execute(sql, (user_id,))
        return bool(int(result.fetchone()[0]))

    def change_new_group(self, user_id: int, new_group: bool) -> None:
        """ Переключаем создание нового пресета """
        sql = """ UPDATE users_info SET new_group = ? WHERE user_id = ? """
        self.cursor.execute(sql, (int(new_group), user_id))
        return self.conn.commit()

    # def get_group_by_preset(self, user_id: int, preset: int):
        # """ Получаем данные о группе по preset_num """
        # sql = """ SELECT group_name, subgroup FROM users
        # WHERE user_id = ? AND preset_num = ? """
        # result = self.cursor.execute(sql, (user_id, preset))
        # print(result)
        # result_list = []
        # for item in result.fetchall():
            # result_list.append(int(item[0]))
        # print(result_list)
        # return result_list

    def del_preset_by_num(self, user_id: int, preset: int) -> None:
        """ Удаляем группу по preset_num """
        sql = """ DELETE FROM users
        WHERE user_id = ? AND preset_num = ? """
        self.cursor.execute(sql, (user_id, preset))
        return self.conn.commit()

    def update_preset_num(self, user_id: int, deleted_preset_num: int) -> None:
        """ Меняем preset_num, где preset_num > deleted_preset_num """
        sql = """ UPDATE users SET preset_num = preset_num - 1
        WHERE user_id = ? AND preset_num > ? """
        self.cursor.execute(sql, (user_id, deleted_preset_num))
        return self.conn.commit()

    def get_on_delete(self, user_id: int) -> int:
        """ Получаем on_delete_page пользователя """
        sql = """ SELECT on_delete_page FROM users_info
        WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        return result.fetchone()[0]

    def change_on_delete(self, user_id: int, on_delete: int) -> None:
        """ Меняем on_delete_page пользователя """
        sql = """ UPDATE users_info SET on_delete_page = ? 
        WHERE user_id = ? """
        self.cursor.execute(sql, (on_delete, user_id))
        return self.conn.commit()

    def get_stage(self, user_id: int) -> str:
        """ Получаем Stage пользователя """
        sql = """ SELECT on_stage FROM users_info
        WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        return result.fetchone()[0]

    def change_stage(self, user_id: int, stage: str) -> None:
        """ Изменяем Stage пользователя """
        sql = """UPDATE users_info SET on_stage = ? 
        WHERE user_id = ? """
        self.cursor.execute(sql, (stage, user_id))
        return self.conn.commit()

    def get_form(self, user_id: int) -> str:
        """ Достаем form пользователя """
        sql = """ SELECT form FROM users 
        WHERE user_id = ? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return str(result.fetchone()[0])

    def change_form(self, user_id: int, form: str) -> None:
        """ Меняем form пользователя """
        sql = """UPDATE users SET form = ? 
        WHERE user_id = ? AND preset_num = ?"""
        self.cursor.execute(sql, (form, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def del_form(self, user_id: int) -> None:
        """ Удаляем form пользователя """
        sql = """ UPDATE users SET form=null 
        WHERE user_id=? AND preset_num = ?"""
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_fac(self, user_id: int) -> str:
        """ Достаем fac пользователя """
        sql = """ SELECT fac FROM users 
        WHERE user_id = ? AND preset_num = ?"""
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return str(result.fetchone()[0])

    def change_fac(self, user_id: int, fac: str) -> None:
        """ Меняем fac пользователя """
        sql = """UPDATE users SET fac = ? 
        WHERE user_id = ? AND preset_num = ?"""
        self.cursor.execute(sql, (fac, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def del_fac(self, user_id: int) -> None:
        """ Удаляем fac пользователя """
        sql = """ UPDATE users SET fac=null 
        WHERE user_id=? AND preset_num = ?"""
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_group_page(self, user_id: int) -> int:
        """ Достаем group_page пользователя """
        sql = """ SELECT group_page FROM users 
        WHERE user_id = ? AND preset_num = ?"""
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])

    def change_group_page(self, user_id: int, group_page: int) -> None:
        """ Меняем group_page пользователя """
        sql = """UPDATE users SET group_page = ? 
        WHERE user_id = ? AND preset_num = ?"""
        self.cursor.execute(sql, (group_page, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_session_group_page(self, user_id: int) -> int:
        """ Достаем session_group_page пользователя """
        sql = """ SELECT session_group_page FROM users 
        WHERE user_id = ? AND preset_num = ?"""
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])

    def change_session_group_page(self, user_id: int, 
            session_group_page: int) -> None:
        """ Меняем session_group_page пользователя """
        sql = """UPDATE users SET session_group_page = ? 
        WHERE user_id = ? AND preset_num = ?"""
        self.cursor.execute(sql, (session_group_page, user_id, 
                        self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_group(self, user_id: int) -> str:
        """ Достаем group пользователя """
        sql = """ SELECT group_name FROM users 
        WHERE user_id=? AND preset_num = ?"""
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return str(result.fetchone()[0])

    def change_group(self, user_id: int, group: str) -> None:
        """ Меняем group пользователя """
        sql = """ UPDATE users SET group_name = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (group, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def del_group(self, user_id: int) -> None:
        """ Удаляем group пользователя """
        sql = """ UPDATE users SET group_name=null 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_subgroup(self, user_id: int) -> str:
        """ Достаем subgroup пользователя """
        sql = """ SELECT subgroup FROM users 
        WHERE user_id=? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return str(result.fetchone()[0])

    def change_subgroup(self, user_id: int, subgroup: str) -> None:
        """ Меняем subgroup пользователя """
        sql = """ UPDATE users SET subgroup = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (subgroup, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def del_subgroup(self, user_id: int) -> None:
        """ Удаляем subgroup пользователя """
        sql = """ UPDATE users SET subgroup=null 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_quality(self, user_id: int) -> int:
        """ Получаем quality пользователя """
        sql = """ SELECT quality FROM users_info 
        WHERE user_id=? """
        result = self.cursor.execute(sql, (user_id,))
        return int(result.fetchone()[0])
    
    def change_quality(self, user_id: int) -> None:
        """ Меняем quality пользователя """
        if self.get_quality(user_id=user_id) == 1:
            sql = """ UPDATE users_info SET quality=2 
            WHERE user_id=? """
        else:
            sql = """ UPDATE users_info SET quality=1 
            WHERE user_id=? """
        self.cursor.execute(sql, (user_id,))
        return self.conn.commit()

    def get_mode(self, user_id: int) -> str:
        """ Получаем mode пользователя """
        sql = """ SELECT mode FROM users_info 
        WHERE user_id=? """
        result = self.cursor.execute(sql, (user_id,))
        return str(result.fetchone()[0])

    def change_mode(self, user_id: int) -> None:
        """ Меняем mode пользователя """
        if self.get_mode(user_id=user_id) == "night":
            sql = """ UPDATE users_info SET mode = "day" 
            WHERE user_id=? """
        else:
            sql = """ UPDATE users_info SET mode = "night" 
            WHERE user_id=? """
        self.cursor.execute(sql, (user_id,))
        return self.conn.commit()

    def get_week_page(self, user_id: int) -> int:
        """ Получаем week_page пользователя """
        sql = """ SELECT week_page FROM users 
        WHERE user_id=? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])
    
    def change_week_page(self, user_id: int, week_page: int) -> None:
        """ Меняем week_page пользователя """
        sql = """ UPDATE users SET week_page = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (week_page, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_date_page(self, user_id: int) -> int:
        """ Получаем date_page пользователя """
        sql = """ SELECT date_page FROM users 
        WHERE user_id=? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])
    
    def change_date_page(self, user_id: int, date_page: int) -> None:
        """ Меняем date_page пользователя """
        sql = """ UPDATE users SET date_page = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (date_page, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_daily_mail(self, user_id: int) -> int:
        """ Получаем daily_mail пользователя """
        sql = """ SELECT daily_mail FROM users 
        WHERE user_id=? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])
    
    def change_daily_mail(self, user_id: int, daily_mail: int) -> None:
        """ Меняем daily_mail пользователя """
        sql = """ UPDATE users SET daily_mail = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (daily_mail, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_all_daily_mail(self) -> list:
        """ Достаем данные пользователей с daily_mail = 1 """
        sql = """ SELECT user_id, form, fac, group_name, subgroup FROM users 
        WHERE daily_mail=1 AND subgroup IS NOT NULL"""
        result_list = self.cursor.execute(sql)
        result = result_list.fetchall()
        return result

    def get_weekly_mail(self, user_id: int) -> int:
        """ Получаем weekly_mail пользователя """
        sql = """ SELECT weekly_mail FROM users 
        WHERE user_id=? AND preset_num = ? """
        result = self.cursor.execute(sql, (user_id, self.get_preset(user_id=user_id)))
        return int(result.fetchone()[0])
    
    def change_weekly_mail(self, user_id: int, weekly_mail: int) -> None:
        """ Меняем weekly_mail пользователя """
        sql = """ UPDATE users SET weekly_mail = ? 
        WHERE user_id=? AND preset_num = ? """
        self.cursor.execute(sql, (weekly_mail, user_id, self.get_preset(user_id=user_id)))
        return self.conn.commit()

    def get_all_weekly_mail(self) -> list:
        """ Достаем данные пользователей с weekly_mail = 1 """
        sql = """ SELECT user_id, form, fac, group_name, subgroup FROM users 
        WHERE weekly_mail=1 AND subgroup IS NOT NULL"""
        result_list = self.cursor.execute(sql)
        result = result_list.fetchall()
        return result

    def get_passwords(self, user_id: int) -> list:
        """ Получаем пароли пользователя """
        sql = """ SELECT password FROM passwords 
        WHERE user_id = ? """
        result = self.cursor.execute(sql, (user_id,))
        passwords = []
        for item in result.fetchall():
            passwords.append(str(item[0]))
        return passwords

    def _set_creator(self, creator_id: int, password: str) -> None:
        """ Меняем создателя пароля """
        sql = """ UPDATE passwords SET creator_id = ? WHERE password = ? """
        self.cursor.execute(sql, (creator_id, password))
        return self.conn.commit()
    
    def get_creator(self, password: str) -> int | None:
        """ Получаем создателя пароля """
        sql = """ SELECT creator_id FROM passwords WHERE password = ? """
        result = self.cursor.execute(sql, (password,))
        try:
            result = result.fetchone()[0]
        except:
            result = None
        return result

    def add_password(self, user_id: int, password: str) -> Optional[int]:
        """ Проверяем, есть ли этот пароль у пользователя """
        if len(password.split(' ')) > 1:
            return 0
        passwords = self.get_passwords(user_id=user_id)
        success: Optional[int] = True
        for item in passwords:
            if password == item:
                success_code = 102
                return success_code
        if success:
            """ Получаем user_id создателя пароля """
            creator = self.get_creator(password=password)
            """ Добавляем пароль пользователю """
            if creator == None:
                creator = user_id
                sql = """INSERT INTO passwords (user_id, password, creator_id) VALUES (?, ?, ?) """
                self.cursor.execute(sql, (user_id, password, creator))
            else:
                privacy = self.get_privacy(password=password)
                if not str(privacy) == "None":
                    sql = """INSERT INTO passwords (user_id, password, creator_id, privacy) VALUES (?, ?, ?, ?) """
                    self.cursor.execute(sql, (user_id, password, creator, privacy))
                else:
                    success = 101
            self.conn.commit()
        return success

    def get_privacy(self, password: str) -> int | None:
        """ Получаем privacy пароля """
        sql = """ SELECT privacy FROM passwords WHERE password=? """
        result = self.cursor.execute(sql, (password,))
        return result.fetchall()[0][0]

    def set_privacy(self, user_id: int, privacy: int) -> str:
        """ Изменяем privacy пароля """
        sql = """ SELECT password FROM passwords 
        WHERE user_id=? AND creator_id=? AND privacy IS NULL"""
        password = self.cursor.execute(sql, (user_id, user_id))
        password = password.fetchone()[0]
        sql = """ UPDATE passwords SET privacy=? 
        WHERE user_id=? AND creator_id=? AND privacy IS NULL """
        self.cursor.execute(sql, (privacy, user_id, user_id))
        self.conn.commit()
        return password

    def del_password(self, user_id: int, password: str) -> bool:
        """ Проверяем наличие пароля у пользователя """
        passwords = self.get_passwords(user_id=user_id)
        success = False
        for item in passwords:
            if password == item:
                success = True
        if success:
            """ Удаляем пароль пользователя """
            sql = """ DELETE FROM passwords 
            WHERE user_id = ? 
            AND password = ? """
            self.cursor.execute(sql, (user_id, password))
            self.conn.commit()
        return success

    def get_all_passwords(self, password: str) -> list:
        """ Достаем password=password всех пользователей """
        sql = """ SELECT user_id FROM passwords WHERE password=?"""
        result = self.cursor.execute(sql, (password,))
        result = [int(item[0]) for item in result.fetchall()]
        return result

    def close(self) -> None:
        """Закрываем соединение с БД"""
        self.conn.close()
