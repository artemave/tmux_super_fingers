from ..actions.os_open_action import OsOpenAction
from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from .url_target import UrlTarget


def test_payload_if_file_or_url():
    target = UrlTarget('http://example.com')

    assert target.payload.file_or_url == 'http://example.com'


def test_primarty_action_is_os_open():
    target = UrlTarget('http://example.com')

    assert target.default_primary_action() == OsOpenAction


def test_secondary_action_is_copy_to_clipboard():
    target = UrlTarget('http://example.com')

    assert target.default_secondary_action() == CopyToClipboardAction
