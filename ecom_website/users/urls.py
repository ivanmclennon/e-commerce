from django.urls import path, include

from .views import SellerUpdate


urlpatterns = [
    path("", include("allauth.urls")),
    path("seller/", SellerUpdate.as_view(), name="seller_update"),
]
