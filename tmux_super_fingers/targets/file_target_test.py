from pytest import MonkeyPatch

from .file_target import FileTarget
from ..actions.send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from ..actions.os_open_action import OsOpenAction
from ..actions.copy_to_clipboard_action import CopyToClipboardAction


def test_payload_can_be_sent_to_editor_and_os_open():
    target = FileTarget(file_path='/some/path', line_number=14)

    assert target.payload.file_or_url == '/some/path'
    assert target.payload.file_path == '/some/path'
    assert target.payload.line_number == 14


def test_sends_to_tmux_if_editor_is_nvim(monkeypatch: MonkeyPatch):
    target = FileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'nvim')

    assert target.default_primary_action() == SendToVimInTmuxPaneAction


def test_sends_to_tmux_if_editor_is_vim(monkeypatch: MonkeyPatch):
    target = FileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'vim')

    assert target.default_primary_action() == SendToVimInTmuxPaneAction


def test_sends_to_os_open_if_editor_is_not_vim(monkeypatch: MonkeyPatch):
    target = FileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'code')

    assert target.default_primary_action() == OsOpenAction


def test_secondary_action_is_copy_to_clipboard():
    target = FileTarget('/some/path')

    assert target.default_secondary_action() == CopyToClipboardAction
