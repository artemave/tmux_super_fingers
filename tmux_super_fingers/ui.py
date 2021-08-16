import curses
from abc import ABCMeta, abstractmethod


class UI(metaclass=ABCMeta):  # pragma: no cover
    @property
    @abstractmethod
    def BOLD(self) -> int:
        ...

    @property
    @abstractmethod
    def DIM(self) -> int:
        ...

    @property
    @abstractmethod
    def BLACK_ON_CYAN(self) -> int:
        ...

    @property
    @abstractmethod
    def BLACK_ON_YELLOW(self) -> int:
        ...

    @abstractmethod
    def render_line(self, y: int, x: int, line: str, color: int) -> None:
        ...

    @abstractmethod
    def getch(self) -> int:
        ...


class CursesUI(UI):  # pragma: no cover
    """Curses adapter"""

    @property
    def BOLD(self) -> int: return curses.A_BOLD

    @property
    def DIM(self) -> int: return curses.A_DIM

    @property
    def BLACK_ON_CYAN(self) -> int: return curses.color_pair(1)

    @property
    def BLACK_ON_YELLOW(self) -> int: return curses.color_pair(2)

    def __init__(self, window: curses.window):
        # To inherit window background
        curses.use_default_colors()
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)

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
