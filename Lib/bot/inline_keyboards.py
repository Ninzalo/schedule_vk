from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def bot_info():
    """ Возвращает inline клавиатуру с кнопками 
    "Сообщение разработчику", "Обсуждение" """
    settings = dict(inline=True)
    inline_keyboard = VkKeyboard(**settings)
    inline_keyboard.add_callback_button(
            label='Сообщение разработчику', 
            color=VkKeyboardColor.POSITIVE, 
            payload={
                'type': 'open_link', 
                'link': 'https://vk.com/im?media=&sel=478270913'
                }
            )
    inline_keyboard.add_line()
    inline_keyboard.add_callback_button(
            label='Обсуждение', 
            color=VkKeyboardColor.POSITIVE, 
            payload={
                'type': 'open_link', 
                'link': 'https://vk.com/topic-210110232_48270692'
                }
            )
    return inline_keyboard
