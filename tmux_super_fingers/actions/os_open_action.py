import sys
from ..utils import shell
from .action import Action
from ..targets import OsOpenable


class OsOpenAction(Action):
    target: OsOpenable

    def perform(self) -> None:
        is_macos = 'darwin' in sys.platform.lower()
        os_open = 'open' if is_macos else 'xdg-open'

        shell(f'{os_open} {self.target.file_or_url}')
