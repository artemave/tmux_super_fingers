import os
from typing import Any, Dict, List

import pytest

from ..mark import Mark
from ..pane import Pane
from ..targets import TextFileTarget, UrlTarget

TEXT = """
Rendered layouts/_base.html.erb (Duration: 32.9ms | Allocations: 2204)
Completed 200 OK in 367ms (Views: 316.5ms | ActiveRecord: 23.2ms | Allocations: 40554)


Started GET "/en/orders/1007056676" for ::1 at 2019-11-18 12:49:58 +0100
Processing by OrdersController#show as HTML
  Parameters: {"locale"=>"en", "id"=>"1007056676"}
  Rendered partials/_current_theme.html.erb (Duration: 1.5ms | Allocations: 587)
  Rendered layouts/_base.html.erb (Duration: 40.7ms | Allocations: 3116)
Completed 200 OK in 307ms (Views: 256.6ms | ActiveRecord: 17.5ms | Allocations: 47708)

"""

ORDERS_CONTROLLER = """
class OrdersController
  def index; end

  def show; end
end
"""


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


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


@pytest.fixture(scope="function")
def change_test_dir(tmpdir: str, request: Any) -> None:
    os.chdir(tmpdir)
    yield(tmpdir)
    os.chdir(request.config.invocation_dir)


def test_finds_relative_file(change_test_dir: str):
    text = """
Banana man
Stuff in ./app/controllers/orders_controller.rb rail
Hello
    """
    pane = {
        'unwrapped_text': text,
        'pane_current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=19,
            text='./app/controllers/orders_controller.rb',
            target=TextFileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_relative_file_with_line_number(change_test_dir: str):
    pane = {
        'unwrapped_text': 'Stuff in ./app/controllers/orders_controller.rb:32',
        'pane_current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=9,
            text='./app/controllers/orders_controller.rb:32',
            target=TextFileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                line_number=32
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_absolute_file(change_test_dir: str):
    cwd = os.getcwd()
    pane = {
        'unwrapped_text': f'Stuff in {cwd}/app/controllers/orders_controller.rb hello',
        'pane_current_path': cwd
    }
    expected_marks = [
        Mark(
            start=9,
            text=os.getcwd() + '/app/controllers/orders_controller.rb',
            target=TextFileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb'
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_diff_path(change_test_dir: str):
    text = """
diff --git a/app/controllers/orders_controller.rb b/app/controllers/orders_controller.rb
index c06609e..0f33345 100644
--- a/app/controllers/orders_controller.rb
+++ b/app/controllers/orders_controller.rb
    """
    pane = {
        'unwrapped_text': text,
        'pane_current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=165,
            text='app/controllers/orders_controller.rb',
            target=TextFileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb'
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_rails_controller(change_test_dir: str):
    pane = {
        'unwrapped_text': 'Processing by OrdersController#show as HTML',
        'pane_current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=14,
            text='OrdersController#show',
            target=TextFileTarget(
                file_path=change_test_dir + '/app/controllers/orders_controller.rb',
                line_number=5
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_rails_partial(change_test_dir: str):
    pane = {
        'unwrapped_text': 'Rendered partials/_client_user_bar.html.erb'
        '(Duration: 22.6ms | Allocations: 5429)',
        'pane_current_path': os.getcwd()}
    expected_marks = [
        Mark(
            start=9,
            text='partials/_client_user_bar.html.erb',
            target=TextFileTarget(
                file_path=change_test_dir + '/app/views/partials/_client_user_bar.html.erb'
            )
        )
    ]
    assert_marks(pane, expected_marks, './app/views/partials/_client_user_bar.html.erb')


def test_finds_url():
    pane = create_pane({
        'unwrapped_text': 'Some url https://wfhftw.org yarp',
    })
    expected_marks = [
        Mark(
            start=9,
            text='https://wfhftw.org',
            target=UrlTarget(
                url='https://wfhftw.org'
            )
        )
    ]
    assert pane.marks == expected_marks


def test_skips_duplicate_marks():
    pane = create_pane({
        'unwrapped_text': 'Some url https://wfhftw.org yarp hm https://wfhftw.org yarp',
    })
    expected_marks = [
        Mark(
            start=36,
            text='https://wfhftw.org',
            target=UrlTarget(
                url='https://wfhftw.org'
            )
        )
    ]
    assert pane.marks == expected_marks
