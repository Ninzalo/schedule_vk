from typing import List, NamedTuple, Literal
from Lib.bot.output_texts import error_return_str

colors = Literal['negative', 'positive', 'primary', 'secondary']

class Button(NamedTuple):
    text: str
    color: colors
    new_line_after: bool = False


class InlineButton(NamedTuple):
    text: str
    color: colors
    payload: dict[str, str] 
    new_line_after: bool


class Buttons(object):
    def __init__(self) -> None:
        self.buttons: List[Button] = []

    def add_button(self, text: str, color: colors,
        new_line_after: bool | None = None):
        if new_line_after is None:
            new_line_after = False

        self.buttons.append(Button(
            text=text, color=color, new_line_after=new_line_after))

    def add_line(self):
        if len(self.buttons) == 0:
            raise Exception('No buttons added')
        last_button = self.buttons[-1]
        self.buttons[-1] = Button(
            text=last_button.text,
            color=last_button.color,
            new_line_after=True)


class InlineButtons(object):
    def __init__(self) -> None:
        self.buttons = []

    def add_button(self, text: str, color: colors,
        payload: dict[str, str], new_line_after: bool | None = None):
        if new_line_after is None:
            new_line_after = False

        self.buttons.append(InlineButton(
            text=text, color=color, 
            new_line_after=new_line_after,
            payload=payload))

    def add_line(self):
        if len(self.buttons) == 0:
            raise Exception('No buttons added')
        last_button = self.buttons[-1]
        self.buttons[-1] = InlineButton(
            text=last_button.text,
            color=last_button.color,
            payload=last_button.payload,
            new_line_after=True)
    def remove_line(self):
        if len(self.buttons) == 0:
            raise Exception('No buttons added')
        last_button = self.buttons[-1]
        self.buttons[-1] = InlineButton(
            text=last_button.text,
            color=last_button.color,
            payload=last_button.payload,
            new_line_after=False)


class Return(NamedTuple):
    user_id: List[int] | int
    text: str 
    buttons: Buttons | list = []
    inline_buttons: InlineButtons | list = []
    attachments: list | None = None
    preuploaded_doc: str | None = None


class Returns(object):
    def __init__(self) -> None:
        self.returns: List[Return] = []

    def add_return(self, 
        user_id: List[int] | int,
        text: str | None,
        buttons: Buttons | list = [],
        inline_buttons: InlineButtons | list = [],
        attachments: list | None = None,
        preuploaded_doc: str | None = None):
        if text == None:
            text = error_return_str()
            buttons = []
            inline_buttons = []
            attachments = []
            preuploaded_doc = None

        self.returns.append(Return(user_id=user_id, text=text,
            buttons=buttons, inline_buttons=inline_buttons,
            attachments=attachments, preuploaded_doc=preuploaded_doc))

def error_return(user_id: int) -> Returns:
    result = Returns()
    result.add_return(user_id=user_id, text=error_return_str())
    return result

def fast_return(user_id: int, text: str, buttons: Buttons | list = [],
    inline_buttons: InlineButtons | list = [], 
    attachments: list | None = None,
    preuploaded_doc: str | None = None) -> Returns:
    result = Returns()
    result.add_return(user_id=user_id, text=text, buttons=buttons,
        inline_buttons=inline_buttons, attachments=attachments,
        preuploaded_doc=preuploaded_doc)
    return result
