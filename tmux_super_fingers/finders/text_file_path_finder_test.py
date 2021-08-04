import os
from ..mark import Mark
from ..targets import TextFileTarget
from ..test_utils import assert_marks


def test_finds_relative_file(change_test_dir: str):
    text = """
Banana man
Stuff in ./app/controllers/orders_controller.rb rail
Hello
    """
    pane = {
        'unwrapped_text': text,
        'current_path': os.getcwd()
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
        'current_path': os.getcwd()
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
        'current_path': cwd
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
