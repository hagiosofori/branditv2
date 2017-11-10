from django.conf.urls import url

from .views import print_orders_view


app_name = "print_orders"


urlpatterns = [
    url(r'^new$', print_orders_view.new, name="new"),

    url(r'^(?P<item_id>[0-9]+)/create$', print_orders_view.create, name="create"),

    url(r'^(?P<print_order_id>[0-9]+)/verify$', print_orders_view.verify, name="print_order_verify"),

    url(r'^(?P<print_order_id>[0-9]+)/edit$', print_orders_view.edit, name="print_order_edit"),
]