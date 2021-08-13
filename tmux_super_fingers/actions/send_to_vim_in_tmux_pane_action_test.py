from pytest import MonkeyPatch
from typing import Optional, Dict, Any, List

from ..pane_props import PaneProps
from .send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from ..targets.text_file_target import TextFileTarget
from ..test_utils import create_pane_props, MockTmuxAdapterBase


class MockTmuxAdapter(MockTmuxAdapterBase):
    def __init__(self, commands: Dict[str, PaneProps] = {}):
        super().__init__()
        self.commands = commands

    def find_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        return self.commands.get(command)


def test_sends_keys_to_new_window_running_vim(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('EDITOR', 'vim')
    monkeypatch.setenv('SHELL', '/bin/zsh')

    target = TextFileTarget(file_path='/tmp/file.txt')
    tmux_adapter = MockTmuxAdapter()

    action = SendToVimInTmuxPaneAction(target=target, tmux_adapter=tmux_adapter)
    action.perform()

    assert tmux_adapter.calls == [
        ['new_window', 'vim', " 'vim /tmp/file.txt; /bin/zsh -i'"]
    ]


def test_sends_keys_to_existing_window_running_vim(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('EDITOR', 'vim')
    monkeypatch.setenv('SHELL', '/bin/zsh')

    target = TextFileTarget(file_path='/tmp/file.txt', line_number=2)
    tmux_adapter = MockTmuxAdapter({'vim': create_pane_props({'pane_id': '2'})})

    action = SendToVimInTmuxPaneAction(target=target, tmux_adapter=tmux_adapter)
    action.perform()

    assert tmux_adapter.calls == [
        ['select_window', '2'],
        ['send_keys', '2', 'Escape ":e +2 /tmp/file.txt" Enter zz']
    ]
