import pytest
from typing import Dict, Any
import os
from pprint import pprint
from ..pane import Pane
from ..mark import Mark
from ..targets import UrlTarget, TextFileTarget

TEXT = """
Rendered layouts/_base.html.erb (Duration: 32.9ms | Allocations: 2204)
Completed 200 OK in 367ms (Views: 316.5ms | ActiveRecord: 23.2ms | Allocations: 40554)


Started GET "/en/orders/1007056676" for ::1 at 2019-11-18 12:49:58 +0100
Processing by OrdersController#show as HTML
  Parameters: {"locale"=>"en", "id"=>"1007056676"}
  Client Load (1.4ms)  SELECT "clients".* FROM "clients" WHERE "clients"."subdomain" = $1 LIMIT $2  [["subdomain", "zams"], ["LIMIT", 1]]
  ↳ app/controllers/concerns/tenantable.rb:22:in `current_tenant_is_client_with'
  User Load (1.0ms)  SELECT "users".* FROM "users" WHERE "users"."client_id" = $1 AND "users"."id" = $2 LIMIT $3  [["client_id", 898370464], ["id", 599798772], ["LIMIT", 1]]
  ↳ app/controllers/client_base_controller.rb:48:in `current_user'
  Page Load (1.8ms)  SELECT slug, title FROM "pages" WHERE "pages"."client_id" = $1  [["client_id", 898370464]]
  ↳ app/models/page.rb:19:in `all_slugs_and_titles'
  Order Load (0.6ms)  SELECT "orders".* FROM "orders" WHERE "orders"."client_id" = $1 AND "orders"."user_id" = $2 AND "orders"."id" = $3 LIMIT $4  [["client_id", 898370464], ["user_id", 599798772], ["id", 1007056676], ["LIMIT", 1]]
  ↳ app/controllers/orders_controller.rb:5:in `show'
  Rendering orders/show.html.erb within layouts/application
  LineItem Load (2.0ms)  SELECT "line_items".* FROM "line_items" INNER JOIN "line_item_groups" ON "line_items"."line_item_group_id" = "line_item_groups"."id" WHERE "line_items"."client_id" = $1 AND "line_item_groups"."client_id" = $2 AND "line_item_groups"."order_id" = $3  [["client_id", 898370464], ["client_id", 898370464], ["order_id", 1007056676]]
  ↳ app/models/order.rb:30:in `number_of_items'
  LineItemGroup Load (0.4ms)  SELECT "line_item_groups".* FROM "line_item_groups" WHERE "line_item_groups"."client_id" = $1 AND "line_item_groups"."order_id" = $2  [["client_id", 898370464], ["order_id", 1007056676]]
  ↳ app/models/order.rb:38:in `pending_approval?'
  VetPrescription Load (0.3ms)  SELECT "vet_prescriptions".* FROM "vet_prescriptions" WHERE "vet_prescriptions"."client_id" = $1 AND "vet_prescriptions"."id" = $2 LIMIT $3  [["client_id", 898370464], ["id", 1029531331], ["LIMIT", 1]]
  ↳ app/models/line_item_group.rb:21:in `effective_strategy'
  LineItem Load (1.2ms)  SELECT "line_items".* FROM "line_items" WHERE "line_items"."client_id" = $1 AND "line_items"."line_item_group_id" = $2  [["client_id", 898370464], ["line_item_group_id", 1060584122]]
  ↳ app/views/partials/_order_vet_prescription_table.html.erb:11
  Product Load (1.0ms)  SELECT "products".* FROM "products" WHERE "products"."id" = $1 LIMIT $2  [["id", 979904108], ["LIMIT", 1]]
  ↳ app/models/line_item.rb:15:in `image_url'
  Rendered partials/_order_vet_prescription_table.html.erb (Duration: 26.7ms | Allocations: 3815)
  VetPrescriptionDetail Load (1.4ms)  SELECT "vet_prescription_details".* FROM "vet_prescription_details" WHERE "vet_prescription_details"."client_id" = $1 AND "vet_prescription_details"."vet_prescription_id" = $2 LIMIT $3  [["client_id", 898370464], ["vet_prescription_id", 1029531331], ["LIMIT", 1]]
  ↳ app/views/partials/_vet_prescription_summary.html.erb:1
  Rendered partials/_vet_prescription_summary.html.erb (Duration: 18.3ms | Allocations: 2070)
  Rendered orders/_vet_prescription.html.erb (Duration: 50.7ms | Allocations: 7448)
  ShippingAddress Load (0.5ms)  SELECT "addresses".* FROM "addresses" WHERE "addresses"."client_id" = $1 AND "addresses"."type" = $2 AND "addresses"."id" = $3 LIMIT $4  [["client_id", 898370464], ["type", "ShippingAddress"], ["id", 959340445], ["LIMIT", 1]]
  ↳ app/views/orders/_order_details.html.erb:25
  Dispatch Exists? (0.8ms)  SELECT 1 AS one FROM "dispatches" INNER JOIN "line_item_groups" ON "dispatches"."line_item_group_id" = "line_item_groups"."id" WHERE "dispatches"."client_id" = $1 AND "line_item_groups"."client_id" = $2 AND "line_item_groups"."order_id" = $3 LIMIT $4  [["client_id", 898370464], ["client_id", 898370464], ["order_id", 1007056676], ["LIMIT", 1]]
  ↳ app/views/orders/_order_details.html.erb:33
  Dispatch Load (0.7ms)  SELECT "dispatches".* FROM "dispatches" INNER JOIN "line_item_groups" ON "dispatches"."line_item_group_id" = "line_item_groups"."id" WHERE "dispatches"."client_id" = $1 AND "line_item_groups"."client_id" = $2 AND "line_item_groups"."order_id" = $3  [["client_id", 898370464], ["client_id", 898370464], ["order_id", 1007056676]]
  ↳ app/views/orders/_order_details.html.erb:34:in `sort'
  DispatchStatusUpdate Load (0.6ms)  SELECT "dispatch_status_updates".* FROM "dispatch_status_updates" WHERE "dispatch_status_updates"."client_id" = $1 AND "dispatch_status_updates"."dispatch_id" = $2 ORDER BY id  [["client_id", 898370464], ["dispatch_id", 305891094]]
  ↳ app/views/orders/_order_details.html.erb:44
  Payment Load (0.5ms)  SELECT "payments".* FROM "payments" WHERE "payments"."client_id" = $1 AND "payments"."order_id" = $2  [["client_id", 898370464], ["order_id", 1007056676]]
  ↳ app/views/orders/_order_details.html.erb:63
  Card Load (1.9ms)  SELECT "cards".* FROM "cards" WHERE "cards"."client_id" = $1 AND "cards"."id" = $2 LIMIT $3  [["client_id", 898370464], ["id", 1037122605], ["LIMIT", 1]]
  ↳ app/views/orders/_order_details.html.erb:77
  Rendered orders/_order_details.html.erb (Duration: 111.7ms | Allocations: 22207)
  Rendered orders/show.html.erb within layouts/application (Duration: 151.2ms | Allocations: 27021)
  ClientConfig Load (0.6ms)  SELECT "client_configs".* FROM "client_configs" WHERE "client_configs"."client_id" = $1 ORDER BY "client_configs"."id" DESC LIMIT $2  [["client_id", 898370464], ["LIMIT", 1]]
  ↳ app/models/client_config.rb:53:in `entity'
  Basket Load (0.4ms)  SELECT "baskets".* FROM "baskets" WHERE "baskets"."client_id" = $1 AND "baskets"."user_id" = $2 LIMIT $3  [["client_id", 898370464], ["user_id", 599798772], ["LIMIT", 1]]
  ↳ app/controllers/concerns/basketable.rb:14:in `current_basket'
  CACHE ClientConfig Load (0.1ms)  SELECT "client_configs".* FROM "client_configs" WHERE "client_configs"."client_id" = $1 ORDER BY "client_configs"."id" DESC LIMIT $2  [["client_id", 898370464], ["LIMIT", 1]]
  ↳ app/models/client_config.rb:53:in `entity'
  Rendered partials/_client_user_bar.html.erb (Duration: 22.6ms | Allocations: 5429)
  ActiveStorage::Attachment Load (0.3ms)  SELECT "active_storage_attachments".* FROM "active_storage_attachments" WHERE "active_storage_attachments"."record_id" = $1 AND "active_storage_attachments"."record_type" = $2 AND "active_storage_attachments"."name" = $3 LIMIT $4  [["record_id", 906572757], ["record_type", "ClientConfig"], ["name", "logo_image"], ["LIMIT", 1]]
  ↳ app/views/partials/_client_logo.html.erb:2
  Rendered partials/_client_logo.html.erb (Duration: 7.5ms | Allocations: 1672)
  Rendered partials/_client_logo_bar.html.erb (Duration: 10.3ms | Allocations: 2232)
  Rendered partials/_flash.html.erb (Duration: 2.9ms | Allocations: 186)
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

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def create_pane(pane_obj) -> Pane:
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

def assert_marks(pane_obj, expected_marks, file_path='./app/controllers/orders_controller.rb'):
    pane = create_pane(pane_obj)
    assert len(pane.marks) == 0

    write_file(file_path, ORDERS_CONTROLLER)
    pane = create_pane(pane_obj)
    assert pane.marks == expected_marks

@pytest.fixture(scope="function")
def change_test_dir(tmpdir, request):
    os.chdir(tmpdir)
    yield(tmpdir)
    os.chdir(request.config.invocation_dir)

def test_finds_relative_file(change_test_dir):
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

def test_finds_relative_file_with_line_number(change_test_dir):
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

def test_finds_absolute_file(change_test_dir):
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

def test_finds_diff_path(change_test_dir):
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

def test_finds_rails_controller(change_test_dir):
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

def test_finds_rails_partial(change_test_dir):
    pane = {
        'unwrapped_text': 'Rendered partials/_client_user_bar.html.erb (Duration: 22.6ms | Allocations: 5429)',
        'pane_current_path': os.getcwd()
    }
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
