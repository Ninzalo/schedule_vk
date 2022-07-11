from dataclasses import dataclass
from typing import List

@dataclass
class Cell:
    value: str|List[str]
    row: int
    col: int
    sheet: int
    top_line_style: str 
    bottom_line_style: str
