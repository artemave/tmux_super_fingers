import os
import pytest
from typing import Any


@pytest.fixture(scope="function")
def change_test_dir(tmpdir: str, request: Any) -> None:
    os.chdir(tmpdir)
    yield (tmpdir)
    os.chdir(request.config.invocation_dir)
