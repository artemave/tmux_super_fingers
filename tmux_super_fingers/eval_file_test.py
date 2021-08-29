import os
from . import eval_file
from .test_utils import write_file
from .targets.file_target import FileTarget
from .targets.target_payload import EditorOpenable


def teardown_function():
    if hasattr(FileTarget, 'primary_action'):
        delattr(FileTarget, 'primary_action')


def test_evals_file_in_the_context_of_this_package(change_test_dir: str):
    teardown_function()

    path = change_test_dir + '/code.py'
    code = (
            'import os\n'
            'from .targets.file_target import FileTarget\n'
            'from .actions.action import Action\n'
            'from .targets.target_payload import EditorOpenable\n'
            '\n'
            '\n'
            'class SendToVsCodeAction(Action):\n'
            '    def __init__(self, target_payload: EditorOpenable):\n'
            '        self.target_payload = target_payload\n'
            '\n'
            '    def perform(self):\n'
            f"        os.system(f'touch {change_test_dir}/' + self.target_payload.file_path)\n"
            '\n'
            '\n'
            'FileTarget.primary_action = SendToVsCodeAction\n'
        )

    write_file(path, code)
    eval_file(path)

    FileTarget.primary_action(EditorOpenable('hello.py')).perform()
    assert os.path.exists(f'{change_test_dir}/hello.py')
