from .os_open_action import OsOpenAction
from ..targets.url_target import UrlTargetPayload
from ..test_utils import MockCliAdapterBase


def test_calls_os_open():
    cli_adapter = MockCliAdapterBase()
    action = OsOpenAction(
        target_payload=UrlTargetPayload('http://example.com'),
        cli_adapter=cli_adapter
    )
    action.perform()
    assert cli_adapter.calls == [['os_open', 'http://example.com']]
