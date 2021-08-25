from django.contrib import admin
from django.contrib.auth.models import User

from .models import Seller


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
