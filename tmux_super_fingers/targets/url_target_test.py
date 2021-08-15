from unittest.mock import patch, MagicMock

from .url_target import UrlTarget


class MockOsOpenAction:
    def perform(self):
        self.performed = True


@patch('tmux_super_fingers.actions.os_open_action.OsOpenAction')
def test_url_target_calls_or_open(OsOpenAction: MagicMock):
    mock_os_open_action = MockOsOpenAction()
    OsOpenAction.return_value = mock_os_open_action

    target = UrlTarget('http://example.com')

    target.perform_primary_action()

    OsOpenAction.assert_called_once_with(target)
    assert mock_os_open_action.performed
