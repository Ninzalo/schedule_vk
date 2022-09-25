import json

from Lib.bot.output_texts import passwords_info_str
from Lib.bot.output_texts import short_description
from Lib.bot.output_texts import messages_str
from Lib.bot.callback_messages import teacher_search_request
from Lib.bot.bot_return import fast_return

from Lib.bot.BotDB_Func import BotDB_Func

# from config import db_path

db = BotDB_Func()
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')


def _edit_message(vk, event, text: str) -> None:
    vk.messages.edit(
        peer_id=event.object.peer_id,
        message=text,
        conversation_message_id=event.object.conversation_message_id)

def callback_func(event, vk):
    if event.object.payload.get('type') in CALLBACK_TYPES:
        vk.messages.sendMessageEventAnswer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id,
            event_data=json.dumps(event.object.payload))

    elif event.object.payload.get('type') == 'what_is_password':
        text = passwords_info_str()
        _edit_message(vk=vk, event=event, text=text)

    elif event.object.payload.get('type') == 'add_new_preset':
        text = 'Группа сохранена'
        db.change_new_group(user_id=event.object.user_id, new_group=True)
        _edit_message(vk=vk, event=event, text=text)

    elif event.object.payload.get('type') == 'short_description':
        text = short_description()
        _edit_message(vk=vk, event=event, text=text)

    elif event.object.payload.get('type') == 'message_example':
        text = messages_str()
        _edit_message(vk=vk, event=event, text=text)

    elif event.object.payload.get('type') == 'next_teacher_page':
        return teacher_search_request(
            user_id=event.object.user_id,
            edit='next_teacher')

    elif event.object.payload.get('type') == 'prev_teacher_page':
        return teacher_search_request(
            user_id=event.object.user_id,
            edit='prev_teacher')

    elif event.object.payload.get('type') == 'next_data_page':
        return teacher_search_request(
            user_id=event.object.user_id,
            edit='next_page')

    elif event.object.payload.get('type') == 'prev_data_page':
        return teacher_search_request(
            user_id=event.object.user_id,
            edit='prev_page')

    elif event.object.payload.get('type') == 'first_data_page':
        return teacher_search_request(
            user_id=event.object.user_id,
            edit='first_page')

    elif event.object.payload.get('type') == 'fake_button':
        return fast_return(user_id=event.object.user_id,
            text='Это не кнопка с:')
