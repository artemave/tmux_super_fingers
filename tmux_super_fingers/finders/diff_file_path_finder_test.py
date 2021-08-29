import os

from ..mark import Mark
from ..targets.file_target import FileTarget, ContentType
from ..test_utils import assert_marks


def test_finds_diff_path(change_test_dir: str):
    text = """
diff --git a/app/controllers/orders_controller.rb b/app/controllers/orders_controller.rb
index c06609e..0f33345 100644
--- a/app/controllers/orders_controller.rb
+++ b/app/controllers/orders_controller.rb
    """
    pane = {
        'unwrapped_text': text,
        'current_path': os.getcwd()
    }
    expected_marks = [
        Mark(
            start=165,
            text='app/controllers/orders_controller.rb',
            target=FileTarget(
                file_path=os.getcwd() + '/app/controllers/orders_controller.rb',
                content_type=ContentType.TEXT
            )
        )
    ]
    assert_marks(pane, expected_marks)
