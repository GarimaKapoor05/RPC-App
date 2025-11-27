from django.urls import path, include
from .views import ProfileView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("profile/", ProfileView.as_view()),
]
