from abc import ABCMeta, abstractmethod
from typing import Optional
import re
import os

from .pane_props import PaneProps
from .utils import shell


class TmuxAdapter(metaclass=ABCMeta):
    @abstractmethod
    def find_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        ...

    @abstractmethod
    def select_window(self, id: str) -> None:
        ...

    @abstractmethod
    def send_keys(self, id: str, keys: str) -> None:
        ...

    @abstractmethod
    def new_window(self, name: str, command: str) -> None:
        ...


class RealTmuxAdapter(TmuxAdapter):
    def find_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        session_panes_props = PaneProps.session_panes_props()

        tty_list = [pane_props.pane_tty for pane_props in session_panes_props]

        tty_infos = shell(f"ps -o state= -o comm= -o tty= -t {','.join(tty_list)}").split('\n')

        process_info = next(iter([
            info for info in tty_infos if re.search(fr'^[^TXZ] +{command}', info)
        ]), None)

        if process_info:
            pane_tty = re.split(' +', process_info)[-1]
            return [
                pane_props for pane_props in session_panes_props
                if pane_props.pane_tty == f'/dev/{pane_tty}'
            ][0]

    def select_window(self, id: str) -> None:
        os.system(f'tmux select-window -t {id}')

    def send_keys(self, id: str, keys: str) -> None:
        os.system(f'tmux send-keys -t {id} {keys}')

    def new_window(self, name: str, command: str) -> None:
        os.system(f'tmux new-window -n {name} {command}')
