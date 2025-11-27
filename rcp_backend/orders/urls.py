from django.urls import path
from .views import CreateOrderView, UserOrdersView, OrderDetailView

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("my-orders/<str:email>/", UserOrdersView.as_view(), name="user-orders"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
]
