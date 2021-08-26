from django.contrib import admin

from .models import ItemProxy, AutoProxy, ServiceProxy


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
