import json

from Lib.bot.output_texts import passwords_info_str
from Lib.bot.output_texts import short_description
from Lib.bot.output_texts import messages_str

from Lib.bot.BotDB_Func import BotDB_Func

from config import db_path

db = BotDB_Func(db_path=db_path)
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

def callback_func(event, vk):
    if event.object.payload.get('type') in CALLBACK_TYPES:
        vk.messages.sendMessageEventAnswer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id,
            event_data=json.dumps(event.object.payload)
            )

    elif event.object.payload.get('type') == 'what_is_password':
        text = passwords_info_str()
        vk.messages.edit(
            peer_id=event.object.peer_id,
            message=text,
            conversation_message_id=event.object.conversation_message_id
            )

    elif event.object.payload.get('type') == 'add_new_preset':
        text = 'Группа сохранена'
        db.change_new_group(user_id=event.object.user_id, new_group=True)
        vk.messages.edit(
            peer_id=event.object.peer_id,
            message=text,
            conversation_message_id=event.object.conversation_message_id
            )

    elif event.object.payload.get('type') == 'short_description':
        text = short_description()
        vk.messages.edit(
            peer_id=event.object.peer_id,
            message=text,
            conversation_message_id=event.object.conversation_message_id
            )

    elif event.object.payload.get('type') == 'message_example':
        text = messages_str()
        vk.messages.edit(
            peer_id=event.object.peer_id,
            message=text,
            conversation_message_id=event.object.conversation_message_id
            )

