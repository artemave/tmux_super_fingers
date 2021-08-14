from .os_open_action import OsOpenAction
from ..targets.url_target import UrlTarget
from ..test_utils import MockTmuxAdapterBase


def test_calls_os_open():
    tmux_adapter = MockTmuxAdapterBase()
    action = OsOpenAction(target=UrlTarget('http://example.com'), tmux_adapter=tmux_adapter)
    action.perform()
    assert tmux_adapter.calls == [['os_open', 'http://example.com']]
