from django.urls import path, include

from .views import (
    index,
    ItemList,
    AutoList,
    ServiceList,
    ItemDetail,
    AutoDetail,
    ServiceDetail,
    ItemCreate,
    AutoCreate,
    ServiceCreate,
    ItemUpdate,
    AutoUpdate,
    ServiceUpdate,
)


urlpatterns = [
    path("", index, name="index"),
    path("items/", ItemList.as_view(), name="items_list"),
    path("cars/", AutoList.as_view(), name="cars_list"),
    path("services/", ServiceList.as_view(), name="services_list"),
    path("items/<int:pk>", ItemDetail.as_view(), name="item_detail"),
    path("cars/<int:pk>", AutoDetail.as_view(), name="car_detail"),
    path("services/<int:pk>", ServiceDetail.as_view(), name="service_detail"),
    path("items/add/", ItemCreate.as_view(), name="create_item"),
    path("items/<int:pk>/edit/", ItemUpdate.as_view(), name="update_item"),
    path("cars/add/", AutoCreate.as_view(), name="create_car"),
    path("cars/<int:pk>/edit/", AutoUpdate.as_view(), name="update_car"),
    path("services/add/", ServiceCreate.as_view(), name="create_service"),
    path("services/<int:pk>/edit/", ServiceUpdate.as_view(), name="update_service"),
]
