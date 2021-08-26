from django.urls import path, include

from .views import subscribe_view


urlpatterns = [
    path("", subscribe_view, name="subscribe"),
]
