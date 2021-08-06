import os

from ..targets.text_file_target import TextFileTarget
from ..mark import Mark
from ..test_utils import assert_marks

"""
Example rails log:

Rendered layouts/_base.html.erb (Duration: 32.9ms | Allocations: 2204)
Completed 200 OK in 367ms (Views: 316.5ms | ActiveRecord: 23.2ms | Allocations: 40554)


Started GET "/en/orders/1007056676" for ::1 at 2019-11-18 12:49:58 +0100
Processing by OrdersController#show as HTML
  Parameters: {"locale"=>"en", "id"=>"1007056676"}
  Rendered partials/_current_theme.html.erb (Duration: 1.5ms | Allocations: 587)
  Rendered layouts/_base.html.erb (Duration: 40.7ms | Allocations: 3116)
Completed 200 OK in 307ms (Views: 256.6ms | ActiveRecord: 17.5ms | Allocations: 47708)

"""


def test_finds_rails_controller(change_test_dir: str):
    pane = {
            'unwrapped_text': 'Processing by OrdersController#show as HTML',
            'current_path': os.getcwd()
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
