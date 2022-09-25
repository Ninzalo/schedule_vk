from Lib.bot.bot_return import Returns, Return
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Lib.bot.elapsed_time import elapsed_time

@elapsed_time
def _message_send(vk_session, message: Return) -> None:
    post = {
        'user_id': message.user_id,
        'random_id': 0
    }

    if message.text is not None:
        post['message'] = message.text

    if message.buttons != []:
        keyboard = VkKeyboard()
        for button in message.buttons.buttons:
            if button.color == 'primary':
                color = VkKeyboardColor.PRIMARY
            elif button.color == 'positive':
                color = VkKeyboardColor.POSITIVE
            elif button.color == 'negative':
                color = VkKeyboardColor.NEGATIVE
            else:
                color = VkKeyboardColor.SECONDARY
            keyboard.add_button(label=button.text, 
                color=color)
            if button.new_line_after is True:
                keyboard.add_line()
        post["keyboard"] = keyboard.get_keyboard()

    if message.inline_buttons != []:
        settings = dict(one_time=False, inline=True)
        inline_keyboard = VkKeyboard(**settings)
        for i_button in message.inline_buttons.buttons:
            if i_button.color == 'primary':
                color = VkKeyboardColor.PRIMARY
            elif i_button.color == 'positive':
                color = VkKeyboardColor.POSITIVE
            elif i_button.color == 'negative':
                color = VkKeyboardColor.NEGATIVE
            else:
                color = VkKeyboardColor.SECONDARY
            inline_keyboard.add_callback_button(label=i_button.text,
                color=color,
                payload=i_button.payload)
            if i_button.new_line_after is True:
                inline_keyboard.add_line()
        post['keyboard'] = inline_keyboard.get_keyboard()
    
    if message.preuploaded_doc is not None:
        post['attachment'] = message.preuploaded_doc

    if message.attachments is not None and message.attachments != []:
        post['attachment'] = ''
        for attachment in message.attachments:
            type_of_attachment = attachment['type']
            if type_of_attachment == 'doc':
                post['message'] += f'\n\nФайл: '\
                    f'"{attachment[f"{type_of_attachment}"]["title"]}"'\
                    f'\n{attachment[f"{type_of_attachment}"]["url"].split("&dl")[0]}'
            else:
                attachment_owner_id = attachment[
                    f'{type_of_attachment}']['owner_id']
                attachment_id = attachment[f'{type_of_attachment}']['id']
                try:
                    attachment_access_key = attachment[
                        f'{type_of_attachment}']['access_key']
                    post['attachment'] += f'{type_of_attachment}'\
                        f'{attachment_owner_id}_{attachment_id}'\
                        f'_{attachment_access_key},'
                except:
                    post['attachment'] += f'{type_of_attachment}'\
                        f'{attachment_owner_id}_{attachment_id},'

    vk_session.method('messages.send', post)

class Sender:
    def __init__(self, vk_session):
        self.vk_session = vk_session

    def sender(self, messages: Returns):
        for message in messages.returns:
            try:
                _message_send(vk_session=self.vk_session, message=message)
            except Exception as _ex:
                print(f'[INFO] Failed to send message '\
                    f'to {message.user_id} | {_ex}')
