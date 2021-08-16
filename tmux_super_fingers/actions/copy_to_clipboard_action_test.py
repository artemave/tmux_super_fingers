from .copy_to_clipboard_action import CopyToClipboardAction
from ..targets.url_target import UrlTarget
from ..test_utils import MockTmuxAdapterBase


def test_calls_copy_to_clipboard():
    tmux_adapter = MockTmuxAdapterBase()
    action = CopyToClipboardAction(target=UrlTarget('http://example.com'), tmux_adapter=tmux_adapter)
    action.perform()
    assert tmux_adapter.calls == [['copy_to_clipboard', 'http://example.com']]
