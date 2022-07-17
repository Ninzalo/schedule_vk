from typing import NamedTuple, List


class Event_hint(NamedTuple):
    msg: str
    message: str
    id: int
    peer_id: int
    button_actions: List[str]|None 
    attachments: list|None = None
