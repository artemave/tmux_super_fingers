import os
from typing import Dict, Any, List
from .pane import Pane
from .mark import Mark
from .pane_props import PaneProps


ORDERS_CONTROLLER = """
class OrdersController
  def index; end

  def show; end
end
"""


def create_pane(pane_obj: Dict[str, Any]) -> Pane:
    pane: Dict[str, Any] = {
        'text': 'some text',
        'unwrapped_text': 'some text',
        'current_path': os.getcwd(),
        'left': 0,
        'right': 0,
        'top': 0,
        'bottom': 0
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
