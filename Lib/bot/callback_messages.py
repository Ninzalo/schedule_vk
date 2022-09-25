from typing import Literal
# from Lib.bot.event_hint import Event_hint
from Lib.bot.output_texts import error_teachers_str 
from Lib.bot.inline_keyboards import teacher_search_kb 
from Lib.bot.BotDB_Func import Teacher_search 
from Lib.bot.teachers import search_fetch, full_search_string
from Lib.bot.bot_return import Returns, fast_return

ts = Teacher_search()


def teacher_search_request(user_id: int,
    name: str | None = None, edit: Literal['next_teacher', 'prev_teacher',
    'next_page', 'prev_page', 'first_page'] | None = None) -> Returns:
    result = Returns()
    if name is not None:
        if len(str(name).strip()) < 3:
            return fast_return(user_id=user_id,
                text=error_teachers_str(name=name))
        if ts.get_full_search(user_id=user_id):
            return fast_return(user_id=user_id,
                text=full_search_string(name=name))
        ts.change_data_page(user_id=user_id, page=0)
        ts.change_teacher_page(user_id=user_id, page=0)
        ts.change_name(user_id=user_id, name=name)
        requested_name = name
    else:
        requested_name = ts.get_name(user_id=user_id)
    if edit == 'next_teacher':
        teacher_page = ts.get_teacher_page(user_id=user_id)
        ts.change_teacher_page(user_id=user_id, page=teacher_page+1)
        ts.change_data_page(user_id=user_id, page=0)
    elif edit == 'prev_teacher':
        teacher_page = ts.get_teacher_page(user_id=user_id)
        ts.change_teacher_page(user_id=user_id, page=teacher_page-1)
        ts.change_data_page(user_id=user_id, page=0)
    elif edit == 'next_page':
        data_page = ts.get_data_page(user_id=user_id)
        ts.change_data_page(user_id=user_id, page=data_page+1)
    elif edit == 'prev_page':
        data_page = ts.get_data_page(user_id=user_id)
        ts.change_data_page(user_id=user_id, page=data_page-1)
    elif edit == 'first_page':
        data_page = ts.get_data_page(user_id=user_id)
        ts.change_data_page(user_id=user_id, page=0)
    teacher_page = ts.get_teacher_page(user_id=user_id)
    data_page = ts.get_data_page(user_id=user_id)
    text, max_teachers, max_pages = search_fetch(
        teacher_page=teacher_page,
        data_page=data_page, name=requested_name)
    if data_page > max_pages or data_page < 0:
        text = f'Ошибка выбора страницы\n\n'
        if data_page > max_pages:
            data_page = max_pages
        elif data_page < 0:
            data_page = 0
        ts.change_data_page(user_id=user_id, page=data_page)
        adding_text, max_teachers, max_pages = search_fetch(
            teacher_page=teacher_page,
            data_page=data_page, name=requested_name)
        text += adding_text
    if teacher_page > max_teachers or teacher_page < 0:
        text = f'Ошибка выбора преподавателя\n\n'
        if teacher_page > max_teachers:
            teacher_page = max_teachers
        elif teacher_page < 0:
            teacher_page = 0 
        ts.change_teacher_page(user_id=user_id, page=teacher_page)
        adding_text, max_teachers, max_pages = search_fetch(
            teacher_page=teacher_page,
            data_page=data_page, name=requested_name)
        text += adding_text
    i_buttons = teacher_search_kb(data_page=data_page, 
        max_data_page=max_pages, teacher_page=teacher_page, 
        max_teacher_num=max_teachers)
    result.add_return(user_id=user_id, text=text,
        inline_buttons=i_buttons)
    return result
