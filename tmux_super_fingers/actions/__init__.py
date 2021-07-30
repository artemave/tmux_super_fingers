import os
import re
from typing import Type
from ..targets import TextFileTarget, Target
from .action import Action
from .os_open_action import OsOpenAction
from .send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction

# TODO: actions from config


def action_for_target_type(klass: Type[Target]) -> Type[Action]:
    if klass is TextFileTarget and re.search('^n?vim', os.environ['EDITOR']):
        return SendToVimInTmuxPaneAction
    else:
        return OsOpenAction
