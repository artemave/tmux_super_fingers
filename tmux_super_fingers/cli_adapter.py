from abc import ABCMeta, abstractmethod
import sys
from typing import Optional, List
import re
import os
import subprocess

from .pane_props import PaneProps
from .utils import shell, strip

is_macos = 'darwin' in sys.platform.lower()


class CliAdapter(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def find_tmux_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        ...

    @abstractmethod
    def select_tmux_window(self, id: str) -> None:
        ...

    @abstractmethod
    def tmux_send_keys(self, id: str, keys: str) -> None:
        ...

    @abstractmethod
    def new_tmux_window(self, name: str, command: str) -> None:
        ...

    @abstractmethod
    def current_tmux_window_panes_props(self) -> List[PaneProps]:
        ...

    @abstractmethod
    def capture_tmux_viewport(self, pane_id: str, start: int, end: int, unwrapped: bool = False) -> str:
        ...

    @abstractmethod
    def get_tmux_pane_cwd(self, pane_tty: str) -> str:
        ...

    @abstractmethod
    def os_open(self, file_or_url: str) -> None:
        ...

    @abstractmethod
    def copy_to_clipboard(self, text: str) -> None:
        ...


class RealCliAdapter(CliAdapter):  # pragma: no cover
    def current_tmux_window_panes_props(self) -> List[PaneProps]:
        return self._get_panes_props('-t !')

    # TODO: there is too much logic here: extract into some testable code
    def find_tmux_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        session_panes_props = self._session_panes_props()

        tty_list = [pane_props.pane_tty for pane_props in session_panes_props]

        tty_infos = shell(f"ps -o state= -o comm= -o tty= -t {','.join(tty_list)}").split('\n')

        process_info = next(iter([
            info for info in tty_infos if re.search(fr'^[^TXZ].? +{command}', info)
        ]), None)

        if process_info:
            pane_tty = re.split(' +', process_info.rstrip())[-1]
            return [
                pane_props for pane_props in session_panes_props
                if pane_props.pane_tty == f'/dev/{pane_tty}'
            ][0]

    def select_tmux_window(self, id: str) -> None:
        os.system(f'tmux select-window -t {id}')

    def tmux_send_keys(self, id: str, keys: str) -> None:
        os.system(f'tmux send-keys -t {id} {keys}')

    def new_tmux_window(self, name: str, command: str) -> None:
        os.system(f'tmux new-window -n {name} {command}')

    def capture_tmux_viewport(self, pane_id: str, start: int, end: int, unwrapped: bool = False) -> str:
        wrap_flag = '-J' if unwrapped else ''
        return strip(
            shell(f'tmux capture-pane -p -S {start} -E {end} {wrap_flag} -t {pane_id}')
        )

    def get_tmux_pane_cwd(self, pane_tty: str) -> str:
        pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
        return shell(f'lsof -a -p {pane_shell_pid} -d cwd -Fn').split('\n')[-1][1:]

    def os_open(self, file_or_url: str) -> None:
        os_open = 'open' if is_macos else 'xdg-open'

        shell(f'{os_open} {file_or_url}')

    def copy_to_clipboard(self, text: str) -> None:
        os_copy_to_clipboard = 'pbcopy' if is_macos else 'xclip'
        subprocess.run(os_copy_to_clipboard, shell=True, check=True, text=True, input=text)

    def get_file_type(self, path: str) -> str:
        file_cmd = '/usr/bin/file --mime-type -b' if is_macos else 'file -ib'
        raw = shell(f'{file_cmd} {path}').split('\n')[0]
        raw_type = re.split('/', raw)[0]
        return raw_type

    def _session_panes_props(self) -> List[PaneProps]:
        return self._get_panes_props('-s')

    def _get_panes_props(self, tmux_target: str) -> List[PaneProps]:
        props: List[str] = shell(
            'tmux list-panes ' + tmux_target + ' -F #{pane_id},#{pane_tty},#{pane_left},'
            '#{pane_right},#{pane_top},#{pane_bottom},#{scroll_position}'
        ).split('\n')

        panes_props = map(self._create_pane_props, props)

        return list(panes_props)

    def _create_pane_props(self, props: str) -> PaneProps:
        pane_id, pane_tty, pane_left, pane_right, pane_top, pane_bottom, scroll_position = \
                props.split(',')

        return PaneProps(
            pane_id=pane_id,
            pane_tty=pane_tty,
            pane_left=pane_left,
            pane_right=pane_right,
            pane_top=pane_top,
            pane_bottom=pane_bottom,
            scroll_position=scroll_position
        )
