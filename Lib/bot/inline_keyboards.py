from Lib.bot.bot_return import InlineButtons


def bot_info() -> InlineButtons:
    """ Возвращает inline клавиатуру с кнопками 
    "Сообщение разработчику", "Обсуждение" """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text='Сообщение разработчику', 
        color='positive', 
        payload={
            'type': 'open_link', 
            'link': 'https://vk.com/im?media=&sel=478270913'
            })
    inline_keyboard.add_line()
    inline_keyboard.add_button(
        text='Обсуждение', 
        color='positive', 
        payload={
            'type': 'open_link', 
            'link': 'https://vk.com/topic-210110232_48270692'
            })
    return inline_keyboard


def add_new_preset() -> InlineButtons:
    """ Возвращает inline клавиатуру с подтверждением создания пресета """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text='Да!', 
        color='positive', 
        payload={'type': 'add_new_preset'})
    return inline_keyboard


def message_example() -> InlineButtons:
    """ Возвращает inline клавиатуру с примером ввода сообщения """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text='Пример', 
        color='positive', 
        payload={'type': 'message_example'})
    return inline_keyboard


def passwords_desc() -> InlineButtons:
    """ Возвращает inline клавиатуру с описанием паролей """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text='Узнать', 
        color='positive', 
        payload={'type': 'what_is_password'})
    return inline_keyboard


def short_description() -> InlineButtons: 
    """Возвращает inline клавиатуру с кратким описанием 
    функционала группы """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text='Хочу!', 
        color='positive', 
        payload={'type': 'short_description'})
    return inline_keyboard

def teacher_search_kb(data_page: int, teacher_page: int,
    max_data_page: int, max_teacher_num: int) -> InlineButtons:
    """ Возвращает inline клавиатуру с переключением страниц поиска
    преподователей """
    inline_keyboard = InlineButtons()
    inline_keyboard.add_button(
        text=f'Страница {data_page + 1} / {max_data_page + 1}', 
        color='secondary', 
        payload={'type': 'fake_button'})
    inline_keyboard.add_line()
    add_line = False
    if data_page > 0:
        if data_page > 1:
            inline_keyboard.add_button(
                text=f'< Стр 1', 
                color='positive', 
                payload={'type': 'first_data_page'})
        inline_keyboard.add_button(
            text=f'< Стр {data_page}', 
            color='positive', 
            payload={'type': 'prev_data_page'})
        add_line = True
    if data_page < max_data_page:
        inline_keyboard.add_button(
            text=f'Стр {data_page + 1 + 1} >', 
            color='positive', 
            payload={'type': 'next_data_page'})
        add_line = True
    if add_line:
        inline_keyboard.add_line()
    added_btn = False
    if teacher_page > 0:
        inline_keyboard.add_button(
            text=f'< Препод', 
            color='positive', 
            payload={'type': 'prev_teacher_page'})
        added_btn = True
    if teacher_page < max_teacher_num:
        inline_keyboard.add_button(
            text=f'Препод >', 
            color='positive', 
            payload={'type': 'next_teacher_page'})
        added_btn = True
    if not added_btn:
        inline_keyboard.remove_line()
    return inline_keyboard
