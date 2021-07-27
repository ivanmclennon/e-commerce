from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from ckeditor.widgets import CKEditorWidget


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage
        fields = '__all__'

class FlatPageAdmin(admin.ModelAdmin):

    form = FlatPageAdminForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
