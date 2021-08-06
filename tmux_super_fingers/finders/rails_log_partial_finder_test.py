import os

from ..mark import Mark
from ..targets.text_file_target import TextFileTarget
from ..test_utils import assert_marks


def test_finds_rails_partial(change_test_dir: str):
    pane = {
            'unwrapped_text': 'Rendered partials/_client_user_bar.html.erb'
            '(Duration: 22.6ms | Allocations: 5429)',
            'current_path': os.getcwd()}
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
