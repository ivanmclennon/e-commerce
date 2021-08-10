from .base import ListingList, ListingDetail, ListingCreate, ListingUpdate
from main.models import ServiceListing
from main.forms import ServiceForm


class ServiceList(ListingList):
    model = ServiceListing
    paginate_by = 2


class ServiceDetail(ListingDetail):
    model = ServiceListing


class ServiceCreate(ListingCreate):
    model = ServiceListing
    form_class = ServiceForm


class ServiceUpdate(ListingUpdate):

    model = ServiceListing
    form_class = ServiceForm
