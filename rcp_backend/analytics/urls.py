from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # App APIs
    path('api/pens/', include('pens.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/users/', include('users.urls')),

    # Auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
