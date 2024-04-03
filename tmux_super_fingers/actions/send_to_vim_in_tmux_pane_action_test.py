from pytest import MonkeyPatch
from typing import Optional, Dict

from ..pane_props import PaneProps
from .send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from ..targets.file_target import FileTargetPayload
from ..test_utils import create_pane_props, MockCliAdapterBase


class MockTmuxAdapter(MockCliAdapterBase):
    def __init__(self, commands: Dict[str, PaneProps] = {}):
        super().__init__()
        self.commands = commands

    def find_tmux_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        return self.commands.get(command)


def test_sends_keys_to_new_window_running_vim(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('EDITOR', 'vim')
    monkeypatch.setenv('SHELL', '/bin/zsh')

    target_payload = FileTargetPayload(file_path='/tmp/file.txt')
    cli_adapter = MockTmuxAdapter()

    action = SendToVimInTmuxPaneAction(target_payload, cli_adapter)
    action.perform()

    assert cli_adapter.calls == [
        ['new_tmux_window', 'vim', " 'vim /tmp/file.txt; /bin/zsh -i'"]
    ]


def test_sends_keys_to_existing_window_running_vim(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('EDITOR', 'vim')
    monkeypatch.setenv('SHELL', '/bin/zsh')

    target_payload = FileTargetPayload(file_path='/tmp/file.txt', line_number=2)
    cli_adapter = MockTmuxAdapter({'vim': create_pane_props({'pane_id': '2'})})

    action = SendToVimInTmuxPaneAction(target_payload, cli_adapter)
    action.perform()

    assert cli_adapter.calls == [
        ['select_tmux_window', '2'],
        ['tmux_send_keys', '2', 'Escape ":e +2 /tmp/file.txt" Enter zz'],
        ['select_tmux_pane', '2']
    ]
