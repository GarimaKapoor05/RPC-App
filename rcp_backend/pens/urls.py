from django.urls import path, include
from rest_framework import routers
from .views import PenViewSet, RefillViewSet, get_stock, category_choices

router = routers.DefaultRouter()
router.register(r"pens", PenViewSet, basename="pen")
router.register(r"refills", RefillViewSet, basename="refill")

urlpatterns = [
    path("", include(router.urls)),
    path("pens/<int:pen_id>/stock/", get_stock, name="pen-stock"),
    path("categories/", category_choices, name="category-choices"),
]
