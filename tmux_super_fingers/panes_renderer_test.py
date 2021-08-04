from typing import List, Any

from .test_utils import create_pane
from .panes_renderer import PanesRenderer
from .ui import UI


class MockUI(UI):
    def __init__(self, user_input: List[int]):
        self.calls: List[Any] = []
        self.user_input = user_input

    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        self.calls.append(['render_line', y, x, line, color])

    def refresh(self) -> None:
        self.calls.append(['refresh'])

    def getch(self) -> int:
        return self.user_input.pop(0)


def test_draws_single_pane_with_no_marks_and_exits_on_backspace():
    ui = MockUI(user_input=[127])

    pane = create_pane({'text': 'line 1\nline 2'})
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['refresh'],
    ]
