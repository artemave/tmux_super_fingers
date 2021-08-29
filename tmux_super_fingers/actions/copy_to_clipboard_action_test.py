from .copy_to_clipboard_action import CopyToClipboardAction
from ..targets.url_target import UrlTargetPayload
from ..test_utils import MockCliAdapterBase


def test_calls_copy_to_clipboard():
    cli_adapter = MockCliAdapterBase()
    action = CopyToClipboardAction(
        target_payload=UrlTargetPayload('http://example.com'),
        cli_adapter=cli_adapter
    )
    action.perform()
    assert cli_adapter.calls == [['copy_to_clipboard', 'http://example.com']]
