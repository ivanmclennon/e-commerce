from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from ckeditor.widgets import CKEditorWidget

from .models import (
    Category,
    Picture,
    Tag,
    Seller,
    Listing,
    ItemProxy,
    AutoProxy,
    ServiceProxy,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "slug",
    )
    search_fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


class UserAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_display = (
        "id",
        "username",
        "email",
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_display = ("username", "email")


@admin.register(ItemProxy)
class ItemProxyAdmin(admin.ModelAdmin):
    search_fields = (
        "title",
        "category",
        "seller",
    )
    list_display = (
        "title",
        "category",
        "seller",
        "price",
        "date_created",
        "date_modified",
    )


@admin.register(AutoProxy)
class AutoProxyAdmin(admin.ModelAdmin):
    search_fields = (
        "title",
        "category",
        "seller",
    )
    list_display = (
        "title",
        "category",
        "condition",
        "seller",
        "price",
        "date_created",
    )


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceProxy)
class ServiceProxyAdmin(admin.ModelAdmin):
    search_fields = (
        "title",
        "category",
        "seller",
    )
    list_display = (
        "title",
        "category",
        "place_type",
        "seller",
        "price",
        "date_created",
    )


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = "__all__"


class FlatPageAdmin(admin.ModelAdmin):

    form = FlatPageAdminForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
