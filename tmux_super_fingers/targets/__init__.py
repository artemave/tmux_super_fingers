# flake8: noqa
# type: ignore

# TODO: is there a way to achieve `from .typings import Target, OsOpenable` without disabling type checking/linting?
from .target import Target
from .os_openable import OsOpenable
from .url_target import UrlTarget
from .text_file_target import TextFileTarget
