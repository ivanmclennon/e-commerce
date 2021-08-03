from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ItemListing, AutoListing, ServiceListing


def index(request):
    return render(request, 'index.html')


class ItemList(ListView):
    model = ItemListing


class ItemDetail(DetailView):
    model = ItemListing


class AutoList(ListView):
    model = AutoListing


class AutoDetail(DetailView):
    model = AutoListing


class ServiceList(ListView):
    model = ServiceListing


class ServiceDetail(DetailView):
    model = ServiceListing
