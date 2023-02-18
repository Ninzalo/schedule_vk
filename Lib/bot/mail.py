import json
import datetime
import os
import time
from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.event_hint import Event_hint
from Lib.bot.output_texts import schedule_str

from Lib.bot.bot_getter import week_dates_gen
from Lib.bot.bot_getter import week_schedule
from Lib.bot.bot_getter import get_schedule_path

from Lib.bot.keyboards import stage_mail_keyboard

from Lib.bot.bot_return import Returns, fast_return

# from config import db_path

db = BotDB_Func()


def _send_to_target(
    password: str, user_id: int, text: str, attachments: list | None
) -> Returns:
    target_ids = db.get_all_users_with_pass(password=password)
    result = Returns()
    for target_id in target_ids:
        try:
            result.add_return(
                user_id=target_id, text=text, attachments=attachments
            )
        except:
            error_text = f"Не получилось отправить сообщение @{target_id}"
            result.add_return(user_id=user_id, text=error_text)
    return result


def mail(event: Event_hint, user_id: int) -> Returns:
    result = Returns()
    passwords = db.get_passwords(user_id=user_id)

    for password in passwords:
        if event.message.split(" ")[0] == password:
            password_privacy = db.get_privacy(password=password)
            if password_privacy == 1:
                password_creator = db.get_creator(password=password)
                if password_creator == user_id:
                    text = f"#{password}\n\n"
                    text += event.message.strip(password).strip()
                    attachments = []
                    if event.attachments != []:
                        attachments = event.attachments
                    result.returns += _send_to_target(
                        password=password,
                        user_id=user_id,
                        text=text,
                        attachments=attachments,
                    ).returns
                else:
                    text = (
                        f"Вы не можете делать рассылку "
                        f"по паролю #{password}"
                    )
                    result.add_return(user_id=user_id, text=text)
            elif password_privacy == 0:
                text = f"#{password}\n\n"
                text += event.message.strip(password).strip()

                attachments = []
                if event.attachments != []:
                    attachments = event.attachments

                result.returns += _send_to_target(
                    password=password,
                    user_id=user_id,
                    text=text,
                    attachments=attachments,
                ).returns
    if result.returns == []:
        result.add_return(user_id=user_id, text="Вы не добавили данный пароль")
    return result


def daily_mail() -> Returns:
    result = Returns()
    users_for_daily_mail = db.get_all_daily_mail()
    for user_id, form, fac, group, subgroup in users_for_daily_mail:
        schedule_path = get_schedule_path(form=form, fac=fac, group=group)
        try:
            with open(schedule_path) as f:
                data = json.load(f)
        except:
            continue
        new_data = []
        date_day = int(datetime.datetime.today().strftime("%d"))
        date_month = int(datetime.datetime.today().strftime("%m"))
        date_year = int(f'20{datetime.datetime.today().strftime("%y")}')
        for date in data:
            file_year = int(date["date"].split("-")[0])
            file_month = int(date["date"].split("-")[1])
            file_day = int(date["date"].split("-")[2])
            if file_year > date_year:
                new_data.append(date)
            elif file_year == date_year and file_month > date_month:
                new_data.append(date)
            elif (
                file_year == date_year
                and file_month == date_month
                and file_day >= date_day
            ):
                new_data.append(date)
        if len(new_data) != 0:
            delta = 1
            today_date = datetime.datetime.now()
            next_day_date = today_date + datetime.timedelta(delta)
            next_day_date_day = int(next_day_date.strftime("%d"))
            next_day_date_month = int(next_day_date.strftime("%m"))
            next_day_date_year = int(next_day_date.strftime("%Y"))
            next_day_date_strf = (
                f"{next_day_date_year}-"
                f"{next_day_date_month}-{next_day_date_day}"
            )
            for index in range(0, len(new_data)):
                if new_data[index]["date"] == str(next_day_date_strf):
                    text = f"Расписание на завтра:\n\n"
                    text += schedule_str(
                        data=new_data[index],
                        group=group,
                        subgroup=subgroup,
                        date=new_data[index]["date"],
                    )
                    try:
                        result.add_return(user_id=user_id, text=text)
                        time.sleep(0.2)
                    except:
                        pass
                    break
    return result


def weekly_mail(vk) -> Returns:
    result = Returns()
    users_for_weekly_mail = db.get_all_weekly_mail()
    for user_id, form, fac, group, subgroup in users_for_weekly_mail:
        quality = db.get_quality(user_id=user_id)
        mode = db.get_mode(user_id=user_id)
        first_date, last_date = week_dates_gen(user_week_page=1)
        doc, error = week_schedule(
            vk=vk,
            form=form,
            fac=fac,
            group=group,
            subgroup=subgroup,
            quality=quality,
            mode=mode,
            user_id=user_id,
            first_date=first_date,
            last_date=last_date,
        )
        if error == 0:
            text = "Расписание на следующую неделю:\n"
            text += f"{group} | {subgroup}\n\n"
            text += f"Неделя {first_date} - {last_date}"
            try:
                result.add_return(
                    user_id=user_id, text=text, preuploaded_doc=doc
                )
                time.sleep(0.2)
            except:
                pass
    return result


class MailSettings:
    def change_daily_mail(self, user_id: int) -> Returns:
        if db.get_subgroup(user_id=user_id) != "None":
            if db.get_daily_mail(user_id=user_id) == 0:
                text = "Включена ежедневная рассылка"
                db.change_daily_mail(user_id=user_id, daily_mail=1)
            else:
                text = "Ежедневная рассылка отключена"
                db.change_daily_mail(user_id=user_id, daily_mail=0)
            keyboard = stage_mail_keyboard(
                daily_mail=db.get_daily_mail(user_id=user_id),
                weekly_mail=db.get_weekly_mail(user_id=user_id),
            )
            return fast_return(user_id=user_id, text=text, buttons=keyboard)
        else:
            text = (
                "Для начала выберите свою группу и подгруппу "
                'во вкладке "Расписание"!'
            )
            return fast_return(user_id=user_id, text=text)

    def change_weekly_mail(self, user_id: int) -> Returns:
        if db.get_subgroup(user_id=user_id) != "None":
            if db.get_weekly_mail(user_id=user_id) == 0:
                text = "Включена еженедельная рассылка"
                db.change_weekly_mail(user_id=user_id, weekly_mail=1)
            else:
                text = "Еженедельная рассылка отключена"
                db.change_weekly_mail(user_id=user_id, weekly_mail=0)
            keyboard = stage_mail_keyboard(
                daily_mail=db.get_daily_mail(user_id=user_id),
                weekly_mail=db.get_weekly_mail(user_id=user_id),
            )
            return fast_return(user_id=user_id, text=text, buttons=keyboard)
        else:
            text = (
                "Для начала выберите свою группу и подгруппу "
                'во вкладке "Расписание"!'
            )
            return fast_return(user_id=user_id, text=text)
