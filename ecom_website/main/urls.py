from django.urls import path, include

from .views import (
    index,
    ItemList, AutoList, ServiceList,
    ItemDetail, AutoDetail, ServiceDetail
)


urlpatterns = [
    path('', index, name='index'),
    path('items/', ItemList.as_view(), name='items_list'),
    path('cars/', AutoList.as_view(), name='cars_list'),
    path('services/', ServiceList.as_view(), name='services_list'),
    path('items/<int:pk>', ItemDetail.as_view(), name='item_detail'),
    path('cars/<int:pk>', AutoDetail.as_view(), name='car_detail'),
    path('services/<int:pk>', ServiceDetail.as_view(), name='service_detail'),
]
