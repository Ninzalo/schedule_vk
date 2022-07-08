class Sender:
    def __init__(self, vk_session):
        self.vk_session = vk_session

    def sender(self, id, text=None, preuploaded_doc=None, keyboard=None, inline_keyboard=None, attachments=None):
        post = {
            'user_id': id,
            'random_id': 0
        }

        if text is not None:
            post['message'] = text

        if keyboard is not None:
            post["keyboard"] = keyboard.get_keyboard()

        if inline_keyboard is not None:
            post['keyboard'] = inline_keyboard.get_keyboard()
        
        if keyboard is not None and inline_keyboard is not None:
            post['keyboard'] = keyboard.get_keyboard() and inline_keyboard.get_keyboard()

        if preuploaded_doc is not None:
            post['attachment'] = preuploaded_doc

        if attachments is not None and attachments != []:
            post['attachment'] = ''
            for attachment in attachments:
                type_of_attachment = attachment['type']
                if type_of_attachment == 'doc':
                    post['message'] += f'\n\nФайл: "{attachment[f"{type_of_attachment}"]["title"]}"'\
                            f'\n{attachment[f"{type_of_attachment}"]["url"].split("&dl")[0]}'
                else:
                    attachment_owner_id = attachment[f'{type_of_attachment}']['owner_id']
                    attachment_id = attachment[f'{type_of_attachment}']['id']
                    try:
                        attachment_access_key = attachment[f'{type_of_attachment}']['access_key']
                        post['attachment'] += f'{type_of_attachment}{attachment_owner_id}_{attachment_id}_{attachment_access_key},'
                    except:
                        post['attachment'] += f'{type_of_attachment}{attachment_owner_id}_{attachment_id},'

        self.vk_session.method('messages.send', post)
