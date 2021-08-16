from unittest.mock import patch, MagicMock

from .url_target import UrlTarget


class MockAction:
    def perform(self):
        self.performed = True


@patch('tmux_super_fingers.actions.os_open_action.OsOpenAction')
def test_primarty_action_is_os_open(OsOpenAction: MagicMock):
    mock_action = MockAction()
    OsOpenAction.return_value = mock_action

    target = UrlTarget('http://example.com')

    target.perform_primary_action()

    OsOpenAction.assert_called_once_with(target)
    assert mock_action.performed


@patch('tmux_super_fingers.actions.copy_to_clipboard_action.CopyToClipboardAction')
def test_secondary_action_is_copy_to_clipboard(CopyToClipboardAction: MagicMock):
    mock_action = MockAction()
    CopyToClipboardAction.return_value = mock_action

    target = UrlTarget('http://example.com')

    target.perform_secondary_action()

    CopyToClipboardAction.assert_called_once_with(target)
    assert mock_action.performed
