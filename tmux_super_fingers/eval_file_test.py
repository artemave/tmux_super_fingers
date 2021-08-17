import os

from . import eval_file
from .test_utils import write_file


def test_evals_file_in_the_context_of_this_package(change_test_dir: str):
    path = change_test_dir + '/code.py'
    another_path = change_test_dir + '/hello.txt'
    code = (
            'from .test_utils import write_file\n'
            f'write_file("{another_path}", "hello")'
        )

    write_file(path, code)
    eval_file(path)

    assert os.path.exists(another_path)
