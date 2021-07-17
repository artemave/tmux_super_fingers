from dataclasses import dataclass
from typing import Optional
from .os_openable import OsOpenable
from .target import Target


@dataclass
class _TextFileTarget(Target):
    file_path: str
    line_number: Optional[int] = None

    @property
    def file_or_url(self) -> str:
        return self.file_path


class TextFileTarget(_TextFileTarget, OsOpenable):
    pass

# TODO: interface for "openable in tmux vim"
# For fancy things like zip archives that can also be sent to vim
