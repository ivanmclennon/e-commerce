from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
# from django.contrib.flatpages.admin import FlatPageAdmin

from ckeditor.fields import RichTextField


admin.site.unregister(FlatPage)


class FlatPageAdmin(admin.ModelAdmin):

    content = RichTextField()

    class Meta:
        model = FlatPage


admin.site.register(FlatPage, FlatPageAdmin)
