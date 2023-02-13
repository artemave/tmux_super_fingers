import os
from shutil import copy
from ..mark import Mark
from ..targets.file_target import FileTarget, ContentType
from ..test_utils import assert_marks, create_pane


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
            target=FileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                content_type=ContentType.TEXT
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
            target=FileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                content_type=ContentType.TEXT,
                line_number=32
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_relative_file_with_line_number_python(change_test_dir: str):
    pane = {
        'unwrapped_text': 'File "./app/controllers/orders_controller.rb", line 32, in <module>',
        'current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=6,
            text='./app/controllers/orders_controller.rb", line 32',
            target=FileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                content_type=ContentType.TEXT,
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
            target=FileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                content_type=ContentType.TEXT,
            )
        )
    ]
    assert_marks(pane, expected_marks)


def test_finds_file_with_at_symbol(change_test_dir: str):
    cwd = os.getcwd()
    pane = {
        'unwrapped_text': f'Stuff in {cwd}/app/@controllers/orders_controller.rb hello',
        'current_path': cwd
    }
    expected_marks = [
        Mark(
            start=9,
            text=os.getcwd() + '/app/@controllers/orders_controller.rb',
            target=FileTarget(
                file_path=os.getcwd() + '/app/@controllers/orders_controller.rb',
                content_type=ContentType.TEXT,
            )
        )
    ]
    assert_marks(pane, expected_marks, file_path=f'{cwd}/app/@controllers/orders_controller.rb')


def test_sets_content_type(change_test_dir: str):
    expected_marks = [
        Mark(
            start=9,
            text='./cp',
            target=FileTarget(
                file_path=os.getcwd() + '/cp',
                content_type=ContentType.EXECUTABLE
            )
        )
    ]
    copy('/bin/cp', './')
    pane = create_pane({
        'unwrapped_text': 'Stuff in ./cp rail',
        'current_path': os.getcwd()
    })
    assert pane.marks == expected_marks
