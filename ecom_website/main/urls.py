from django.urls import path, include

from .views import index, ItemList, AutoList, ServiceList


urlpatterns = [
    path('', index, name='index'),
    path('items/', ItemList.as_view()),
    path('cars/', AutoList.as_view()),
    path('services/', ServiceList.as_view()),
]
