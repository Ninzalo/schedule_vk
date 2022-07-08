from typing import NamedTuple


class Event_hint(NamedTuple):
    msg: str
    message: str
    id: int
    peer_id: int
    button_actions: list|None 
    attachments: list|None = None
