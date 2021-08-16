import os
from typing import Dict, Any, List, Optional
from .pane import Pane
from .mark import Mark
from .pane_props import PaneProps
from .tmux_adapter import TmuxAdapter
from .targets.target import Target
from .finders import MarkFinder

ORDERS_CONTROLLER = """
class OrdersController
  def index; end

  def show; end
end
"""


class MockTarget(Target):
    # This is class property, because targets get cloned at some point within the `loop()`
    calls: List[List[Any]] = []

    def perform_primary_action(self):
        self.calls.append(['perform_primary_action'])

    def perform_secondary_action(self):
        self.calls.append(['perform_secondary_action'])


class MockTmuxAdapterBase(TmuxAdapter):  # pragma: no cover
    def __init__(self):
        self.calls: List[List[Any]] = []

    def find_pane_with_running_process(self, command: str) -> Optional[PaneProps]:
        return None

    def select_window(self, id: str) -> None:
        self.calls.append(['select_window', id])

    def new_window(self, name: str, command: str) -> None:
        self.calls.append(['new_window', name, command])

    def send_keys(self, id: str, keys: str) -> None:
        self.calls.append(['send_keys', id, keys])

    def current_window_panes_props(self) -> List[PaneProps]:
        return []

    def capture_viewport(self, pane_id: str, start: int, end: int, unwrapped: bool = False) -> str:
        return ''

    def get_pane_cwd(self, pane_tty: str) -> str:
        return ''

    def os_open(self, file_or_url: str) -> None:
        self.calls.append(['os_open', file_or_url])

    def copy_to_clipboard(self, text: str) -> None:
        self.calls.append(['copy_to_clipboard', text])


def create_pane(pane_obj: Dict[str, Any]) -> Pane:
    pane: Dict[str, Any] = {
        'text': 'some text',
        'unwrapped_text': 'some text',
        'current_path': os.getcwd(),
        'left': 0,
        'right': 0,
        'top': 0,
        'bottom': 0,
        'mark_finder': MarkFinder(),
    }
    pane.update(pane_obj)
    return Pane(**pane)


def create_pane_props(obj: Dict[str, str]) -> PaneProps:
    panes_props = {
        'pane_id': '1',
        'pane_tty': '/dev/tty/9',
        'pane_left': '0',
        'pane_right': '0',
        'pane_top': '0',
        'pane_bottom': '0',
        'scroll_position': '0'
    }
    panes_props.update(obj)
    return PaneProps(**panes_props)


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def assert_marks(
    pane_obj: Dict[str, Any],
    expected_marks: List[Mark],
    file_path: str = './app/controllers/orders_controller.rb'
):
    pane = create_pane(pane_obj)
    assert len(pane.marks) == 0

    write_file(file_path, ORDERS_CONTROLLER)
    pane = create_pane(pane_obj)
    assert pane.marks == expected_marks
