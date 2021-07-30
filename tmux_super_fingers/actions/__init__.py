from typing import Type
from ..targets import UrlTarget, TextFileTarget, Target
from .action import Action
from .os_open_action import OsOpenAction
from .send_to_vim_in_tmux_window_action import SendToVimInTmuxPaneAction

# TODO: actions from config


def action_for_target_type(klass: Type[Target]) -> Type[Action]:
    if klass is UrlTarget:
        return OsOpenAction
    if klass is TextFileTarget:
        return SendToVimInTmuxPaneAction

    raise Exception(f'No action for {klass.__name__}')
