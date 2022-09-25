from typing import Tuple, Literal, List
from Lib.bot.keyboards import stage_start_keyboard
from Lib.bot.bot_getter import get_schedule_path
from Lib.bot.bot_return import Returns, Return, fast_return
from Lib.bot.BotDB_Func import BotDB_Func
from Lib.bot.stages import Pages
from Lib.bot.stages_names import Stages_names
from config import db_path

db = BotDB_Func()
sn = Stages_names()

def all_users_to_reset_page() -> Returns:
    all_users = db.get_users()
    result = Returns()
    for user_id in all_users:
        result.returns += Pages().reset_page(
            user_id=user_id).returns
    return result


def deleted_group(user_id: int) -> Tuple[Literal[0, 1], Returns]:
    form = db.get_form(user_id=user_id)
    group = db.get_group(user_id=user_id)
    fac = db.get_fac(user_id=user_id)
    success = 1
    result = Returns()
    if form != "None" and fac != "None" and group != "None":
        try:
            path = get_schedule_path(form=form, fac=fac, group=group)
            open(path)
            success = 1
        except:
            db.change_stage(user_id=user_id, stage=sn.START)
            db.null_schedule(user_id=user_id)
            text = 'Данные о группе удалены'
            keyboard = stage_start_keyboard()
            success = 0
            result.add_return(user_id=user_id, text=text, 
                buttons=keyboard)
    return success, result
