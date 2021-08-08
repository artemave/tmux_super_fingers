from pytest import MonkeyPatch
from unittest.mock import patch, MagicMock

from .text_file_target import TextFileTarget


def test_file_or_url_is_file_path():
    assert TextFileTarget(file_path='/some/path', line_number=14).file_or_url \
            == '/some/path'


class MockOsOpenAction:
    def perform(self):
        self.performed = True


class MockSendToVimInTmuxPaneAction:
    def perform(self):
        self.performed = True


@patch('tmux_super_fingers.actions.os_open_action.OsOpenAction')
@patch('tmux_super_fingers.actions.send_to_vim_in_tmux_pane_action.SendToVimInTmuxPaneAction')
def test_sends_to_tmux_if_editor_is_nvim(
    SendToVimInTmuxPaneAction: MagicMock,
    OsOpenAction: MagicMock,
    monkeypatch: MonkeyPatch
):
    target = TextFileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'nvim')

    mock_send_to_vim_in_tmux_pane_action = MockSendToVimInTmuxPaneAction()
    SendToVimInTmuxPaneAction.return_value = mock_send_to_vim_in_tmux_pane_action

    target.perform_primary_action()

    SendToVimInTmuxPaneAction.assert_called_once_with(target)
    assert mock_send_to_vim_in_tmux_pane_action.performed
    OsOpenAction.assert_not_called()


@patch('tmux_super_fingers.actions.os_open_action.OsOpenAction')
@patch('tmux_super_fingers.actions.send_to_vim_in_tmux_pane_action.SendToVimInTmuxPaneAction')
def test_sends_to_tmux_if_editor_is_vim(
    SendToVimInTmuxPaneAction: MagicMock,
    OsOpenAction: MagicMock,
    monkeypatch: MonkeyPatch
):
    target = TextFileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'vim')

    mock_send_to_vim_in_tmux_pane_action = MockSendToVimInTmuxPaneAction()
    SendToVimInTmuxPaneAction.return_value = mock_send_to_vim_in_tmux_pane_action

    target.perform_primary_action()

    SendToVimInTmuxPaneAction.assert_called_once_with(target)
    assert mock_send_to_vim_in_tmux_pane_action.performed
    OsOpenAction.assert_not_called()


@patch('tmux_super_fingers.actions.os_open_action.OsOpenAction')
@patch('tmux_super_fingers.actions.send_to_vim_in_tmux_pane_action.SendToVimInTmuxPaneAction')
def test_sends_to_os_open_if_editor_is_not_vim(
    SendToVimInTmuxPaneAction: MagicMock,
    OsOpenAction: MagicMock,
    monkeypatch: MonkeyPatch
):
    target = TextFileTarget(file_path='/some/path')

    monkeypatch.setenv('EDITOR', 'code')

    mock_os_open_action = MockOsOpenAction()
    OsOpenAction.return_value = mock_os_open_action

    target.perform_primary_action()

    OsOpenAction.assert_called_once_with(target)
    assert mock_os_open_action.performed
    SendToVimInTmuxPaneAction.assert_not_called()
