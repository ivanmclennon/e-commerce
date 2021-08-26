from .base import ListingList, ListingUpdate, ListingDetail, ListingCreate
from ..models import ItemListing
from ..forms import ItemForm


class ItemCreate(ListingCreate):

    model = ItemListing
    form_class = ItemForm


class ItemUpdate(ListingUpdate):

    model = ItemListing
    form_class = ItemForm


class ItemList(ListingList):
    model = ItemListing
    paginate_by = 3


class ItemDetail(ListingDetail):
    model = ItemListing
