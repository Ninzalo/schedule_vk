from dataclasses import dataclass
from typing import TypedDict, List


@dataclass
class Other:
    num: str
    name: str
    subgroup: str
    type_of_week: str
    day_of_week: str
    lesson_name: str
    type_of_lesson: str
    room: str
    dates: List[str]|None = None


@dataclass
class Schedule:
    date: str
    all_subgroups: int
    other: Other|None = None
