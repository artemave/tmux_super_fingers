import sys
from ..utils import shell
from .action import Action
from ..targets import OsOpenable

is_macos: bool = 'darwin' in sys.platform.lower()

class OsOpenAction(Action):
    target: OsOpenable

    def perform(self) -> None:
        os_open = 'open' if is_macos else 'xdg-open'
        shell(f'{os_open} {self.target.file_or_url}')
