from curses import ascii
from typing import List, Any

from .test_utils import create_pane
from .panes_renderer import PanesRenderer
from .ui import UI
from .targets.target import Target
from .mark import Mark


class MockTarget(Target):
    # This is class property, because targets get cloned at some point within the `loop()`
    calls: List[List[Any]] = []

    def perform_primary_action(self):
        self.calls.append(['perform_primary_action'])


def teardown_function():
    MockTarget.calls = []


class MockUI(UI):
    def __init__(self, user_input: List[int]):
        self.calls: List[List[Any]] = []
        self.user_input = user_input

    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        self.calls.append(['render_line', y, x, line, color])

    def getch(self) -> int:
        input = self.user_input.pop(0)
        self.calls.append(['getch', input])
        return input


def test_draws_single_pane_with_no_marks_and_exits_on_backspace():
    ui = MockUI(user_input=[ascii.ESC])

    pane = create_pane({'text': 'line 1\nline 2'})
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['getch', ascii.ESC]
    ]


def test_if_no_user_input_backspace_breaks_the_loop():
    ui = MockUI(user_input=[127])
    pane = create_pane({'text': 'line 1\nline 2'})
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['getch', 127],
    ]


def test_draws_single_pane_with_a_single_mark():
    ui = MockUI(user_input=[97])
    mock_target = MockTarget()

    pane = create_pane({'text': 'line 1\nline 2'})
    pane.marks = [Mark(
        start=1,
        text='ine',
        target=mock_target,
        hint='a'
    )]
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['render_line', 0, 1, 'ine', ui.BOLD],
        ['render_line', 0, 1, 'a', ui.BLACK_ON_CYAN],
        ['getch', 97],
    ]
    assert mock_target.calls == [['perform_primary_action']]


def test_hides_marks_that_dont_match_user_input():
    ui = MockUI(user_input=[49, ascii.ESC])
    mock_target = MockTarget()

    pane = create_pane({'text': 'line 1\nline 2'})
    pane.marks = [
        Mark(start=0, text='li', target=mock_target, hint='1a'),
        Mark(start=3, text='e 1', target=mock_target, hint='1b'),
        Mark(start=9, text='e 2', target=mock_target, hint='c'),
    ]
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        # initial render
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 0, 'li', ui.BOLD],
        ['render_line', 0, 0, '1a', ui.BLACK_ON_CYAN],

        ['render_line', 0, 3, 'e 1', ui.BOLD],
        ['render_line', 0, 3, '1b', ui.BLACK_ON_CYAN],

        ['render_line', 1, 3, 'e 2', ui.BOLD],
        ['render_line', 1, 3, 'c', ui.BLACK_ON_CYAN],

        # user pressed '1' - less hints are rendered
        ['getch', 49],

        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 0, 'li', ui.BOLD],
        ['render_line', 0, 1, 'a', ui.BLACK_ON_CYAN],

        ['render_line', 0, 3, 'e 1', ui.BOLD],
        ['render_line', 0, 4, 'b', ui.BLACK_ON_CYAN],

        ['getch', ascii.ESC]
    ]
    assert mock_target.calls == []


def test_shows_back_hidden_marks_when_on_backspace():
    ui = MockUI(user_input=[49, 127, ascii.ESC])
    mock_target = MockTarget()

    pane = create_pane({'text': 'line 1\nline 2'})
    pane.marks = [
        Mark(start=0, text='li', target=mock_target, hint='1a'),
        Mark(start=3, text='e 1', target=mock_target, hint='1b'),
        Mark(start=9, text='e 2', target=mock_target, hint='c'),
    ]
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        # initial render
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 0, 'li', ui.BOLD],
        ['render_line', 0, 0, '1a', ui.BLACK_ON_CYAN],

        ['render_line', 0, 3, 'e 1', ui.BOLD],
        ['render_line', 0, 3, '1b', ui.BLACK_ON_CYAN],

        ['render_line', 1, 3, 'e 2', ui.BOLD],
        ['render_line', 1, 3, 'c', ui.BLACK_ON_CYAN],

        # user pressed '1' - less hints are rendered
        ['getch', 49],

        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 0, 'li', ui.BOLD],
        ['render_line', 0, 1, 'a', ui.BLACK_ON_CYAN],

        ['render_line', 0, 3, 'e 1', ui.BOLD],
        ['render_line', 0, 4, 'b', ui.BLACK_ON_CYAN],

        # user pressed backspace - back to the original
        ['getch', 127],

        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 0, 'li', ui.BOLD],
        ['render_line', 0, 0, '1a', ui.BLACK_ON_CYAN],

        ['render_line', 0, 3, 'e 1', ui.BOLD],
        ['render_line', 0, 3, '1b', ui.BLACK_ON_CYAN],

        ['render_line', 1, 3, 'e 2', ui.BOLD],
        ['render_line', 1, 3, 'c', ui.BLACK_ON_CYAN],

        ['getch', ascii.ESC]
    ]
    assert mock_target.calls == []


def test_multiline_mark():
    ui = MockUI(user_input=[97])
    mock_target = MockTarget()

    pane = create_pane({'text': 'line 1\nline 2'})
    pane.marks = [Mark(
        start=4,
        text='stuff',
        target=mock_target,
        hint='a'
    )]
    panes_renderer = PanesRenderer(ui, [pane])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],
        ['render_line', 0, 4, 'st', ui.BOLD],
        ['render_line', 0, 4, 'a', ui.BLACK_ON_CYAN],
        ['render_line', 1, 0, 'uff', ui.BOLD],
        ['getch', 97],
    ]
    assert mock_target.calls == [['perform_primary_action']]


def test_multiple_panes():
    ui = MockUI(user_input=[ascii.ESC])
    """
    tmux pane border is one character wide
    ┌─────────────────┬────────────────┐
    │0,0              │ 0,10           │
    │                 │                │
    │        1        │        2       │
    │                 │                │
    ├─────────────────┴────────────────┤
    │5,0                               │
    │                                  │
    │                 3                │
    │                                  │
    └──────────────────────────────────┘
    """
    pane1 = create_pane({
        'top': 0,
        'left': 0,
        'right': 8,
        'bottom': 3,
        'text': 'line 1\nline 2'
    })
    pane2 = create_pane({
        'top': 0,
        'left': 10,
        'right': 20,
        'bottom': 3,
        'text': 'line 3\nline 4'
    })
    pane3 = create_pane({
        'top': 5,
        'left': 0,
        'right': 19,
        'bottom': 10,
        'text': 'line 5\nline 6'
    })

    panes_renderer = PanesRenderer(ui, [pane1, pane2, pane3])

    panes_renderer.loop()

    assert ui.calls == [
        ['render_line', 0, 0, 'line 1', ui.DIM],
        ['render_line', 1, 0, 'line 2', ui.DIM],

        ['render_line', 0, 9, '│', ui.DIM],
        ['render_line', 1, 9, '│', ui.DIM],
        ['render_line', 2, 9, '│', ui.DIM],
        ['render_line', 3, 9, '│', ui.DIM],
        ['render_line', 0, 10, 'line 3', ui.DIM],
        ['render_line', 1, 10, 'line 4', ui.DIM],

        ['render_line', 4, 0, '─' * 20, ui.DIM],
        ['render_line', 5, 0, 'line 5', ui.DIM],
        ['render_line', 6, 0, 'line 6', ui.DIM],

        ['getch', ascii.ESC]
    ]
