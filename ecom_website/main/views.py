from django.shortcuts import render

from django.conf import settings

# Create your views here.
def index(request):
    site_in_maintenance = settings.MAINTENANCE_MODE
    return render(request, 'index.html', {
        "site_in_maintenance": site_in_maintenance,
    })