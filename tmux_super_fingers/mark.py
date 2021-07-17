from typing import Optional
from dataclasses import dataclass
from .targets import Target
from .actions import action_for_target_type


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
        action_type = action_for_target_type(type(self.target))
        action_type(self.target).perform()
