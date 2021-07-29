import os
from typing import Dict, Any, List
from ..pane import Pane
from ..mark import Mark


ORDERS_CONTROLLER = """
class OrdersController
  def index; end

  def show; end
end
"""


def create_pane(pane_obj: Dict[str, Any]) -> Pane:
    pane: Dict[str, Any] = {
        'text': 'some text',
        'pane_current_path': os.getcwd(),
        'pane_left': 0,
        'pane_right': 0,
        'pane_top': 0,
        'pane_bottom': 0
    }
    pane.update(pane_obj)
    return Pane(**pane)


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
