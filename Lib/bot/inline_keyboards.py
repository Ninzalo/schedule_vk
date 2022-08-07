from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def bot_info() -> VkKeyboard:
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

def add_new_preset() -> VkKeyboard:
    """ Возвращает inline клавиатуру с подтверждением создания пресета """
    settings = dict(inline=True)
    inline_keyboard = VkKeyboard(**settings)
    inline_keyboard.add_callback_button(
            label='Да!', 
            color=VkKeyboardColor.POSITIVE, 
            payload={'type': 'add_new_preset'}
            )
    return inline_keyboard

def passwords_desc() -> VkKeyboard:
    """ Возвращает inline клавиатуру с описанием паролей """
    settings = dict(inline=True)
    inline_keyboard = VkKeyboard(**settings)
    inline_keyboard.add_callback_button(
            label='Узнать', 
            color=VkKeyboardColor.POSITIVE, 
            payload={'type': 'what_is_password'}
            )
    return inline_keyboard

def short_description() -> VkKeyboard: 
    """ Возвращает inline клавиатуру с кратким описанием функционала группы """
    settings = dict(inline=True)
    inline_keyboard = VkKeyboard(**settings)
    inline_keyboard.add_callback_button(
            label='Хочу!', 
            color=VkKeyboardColor.POSITIVE, 
            payload={'type': 'short_description'}
            )
    return inline_keyboard
