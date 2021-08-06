from typing import List, Any

from .test_utils import create_pane
from .panes_renderer import PanesRenderer
from .ui import UI
from .targets.target import Target
from .mark import Mark


class MockTarget(Target):
    calls: List[List[Any]] = []

    def perform_primary_action(self):
        self.calls.append(['perform_primary_action'])


class MockUI(UI):
    def __init__(self, user_input: List[int]):
        self.calls: List[List[Any]] = []
        self.user_input = user_input

    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        self.calls.append(['render_line', y, x, line, color])

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
    ]


def test_draws_single_pane_with_a_single_mark():
    ui = MockUI(user_input=[97, 127])
    mock_target = MockTarget()

    pane = create_pane({'text': 'line 1\nline 2'})
    pane.marks = [Mark(
        start=2,
        text='ine',
        target=mock_target,
        hint='a'
    )]
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['render_line', 0, 2, 'ine', ui.BOLD],
        ['render_line', 0, 2, 'a', ui.BLACK_ON_CYAN]
    ]
    assert mock_target.calls == [['perform_primary_action']]
