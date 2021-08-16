from typing import Optional
from dataclasses import dataclass
from .targets.target import Target


@dataclass
class Highlight:
    start: int
    text: str

    @property
    def end(self) -> int:
        return self.start + len(self.text)


@dataclass
class Mark(Highlight):
    target: Target
    hint: Optional[str] = None

    def perform_primary_action(self):
        self.target.perform_primary_action()

    def perform_secondary_action(self):
        self.target.perform_secondary_action()
