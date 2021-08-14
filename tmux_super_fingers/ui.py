import curses
from abc import ABCMeta, abstractmethod


class UI(metaclass=ABCMeta):  # pragma: no cover
    BOLD = 101
    DIM = 102
    BLACK_ON_CYAN = 103

    @abstractmethod
    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        ...

    @abstractmethod
    def getch(self) -> int:
        ...


class CursesUI(UI):  # pragma: no cover
    """Curses adapter"""

    BOLD: int = curses.A_BOLD
    DIM: int = curses.A_DIM

    @property
    def BLACK_ON_CYAN(self) -> int:
        return curses.color_pair(1)

    def __init__(self, window: curses.window):
        # To inherit window background
        curses.use_default_colors()
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self.window = window

    # Workaround for:
    # https://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses
    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        try:
            self.window.addstr(y, x, line, color)
        except curses.error:
            self.window.addstr(y, x, line[-1], color)
            self.window.insstr(y, x, line[:-1], color)

        # Refreshing after each render does not seem to affect performance
        self.window.refresh()

    def getch(self) -> int:
        return self.window.getch()
