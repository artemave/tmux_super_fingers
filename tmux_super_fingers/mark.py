from typing import Optional
from dataclasses import dataclass

class MarkTarget:
    pass

@dataclass
class UrlTarget(MarkTarget):
    url: str

@dataclass
class TextFileTarget(MarkTarget):
    file_path: str
    line_number: Optional[int] = None

@dataclass
class Highlight:
    start: int
    text: str

    @property
    def end(self) -> int:
        return self.start + len(self.text)

@dataclass
class Mark(Highlight):
    target: MarkTarget
    hint: Optional[str] = None
