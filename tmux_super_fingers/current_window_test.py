from typing import List, Pattern, Match, Optional
import re

from .pane import Pane
from .mark import Mark
from .pane_props import PaneProps
from .current_window import CurrentWindow
from .test_utils import MockCliAdapterBase, MockTarget
from .finders import MarkFinder
from .finders.finder import BaseFinder


class CharFinder(BaseFinder):
    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile('.')

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span()[0]
        text = match.group(0)

        return Mark(
            start=start,
            text=text,
            target=MockTarget()
        )


def test_panes_from_pane_props():
    class MockTmuxAdapter(MockCliAdapterBase):
        def current_tmux_window_panes_props(self) -> List[PaneProps]:
            return [
                PaneProps(
                    pane_id='1',
                    pane_tty='/dev/tty/1',
                    pane_left='0',
                    pane_top='0',
                    pane_right='9',
                    pane_bottom='10',
                    scroll_position=''
                ),
                PaneProps(
                    pane_id='2',
                    pane_tty='/dev/tty/2',
                    pane_left='11',
                    pane_top='0',
                    pane_right='20',
                    pane_bottom='10',
                    scroll_position='5'
                )
            ]

        def capture_tmux_viewport(self, pane_id: str, start: int, end: int, unwrapped: bool = False) -> str:
            return f'pane_id:{pane_id} start:{start} end:{end} unwrapped:{unwrapped}'

        def get_tmux_pane_cwd(self, pane_tty: str) -> str:
            return '/some/path'

    cli_adapter = MockTmuxAdapter()
    mark_finder = MarkFinder(finders=[CharFinder])
    window = CurrentWindow(cli_adapter, mark_finder)

    assert window.panes == [
        Pane(
            unwrapped_text='pane_id:1 start:0 end:10 unwrapped:True',
            text='pane_id:1 start:0 end:10 unwrapped:False',
            current_path='/some/path',
            left=0,
            right=9,
            top=0,
            bottom=10,
            mark_finder=mark_finder,
        ),
        Pane(
            unwrapped_text='pane_id:2 start:-5 end:5 unwrapped:True',
            text='pane_id:2 start:-5 end:5 unwrapped:False',
            current_path='/some/path',
            left=11,
            right=20,
            top=0,
            bottom=10,
            mark_finder=mark_finder,
        ),
    ]
