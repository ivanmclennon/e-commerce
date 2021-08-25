from typing import Optional, Callable

from django.db.models import QuerySet

from django.urls import reverse
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView

from .models import Seller
from .forms import SellerForm


class SellerUpdate(LoginRequiredMixin, UpdateView):
    """
    UpdateView for updating Seller's information
    """

    model = Seller
    form_class = SellerForm
    login_url = "/accounts/login"
    redirect_field_name = "redirect_to"

    def get_object(self, queryset: Optional[QuerySet] = None) -> Seller:
        return self.model.objects.get(pk=self.request.user.pk)


class CheckUserRightsMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for Listings' CreateViews,
    combines LoginRequired and UserPassesTest
    with custom user banned checker.
    """

    request: HttpRequest

    def get_test_func(self) -> Callable:
        """
        Return check for banned user.
        """
        return self.user_banned_check

    def user_banned_check(self) -> bool:
        """
        Check is user is banned.
        """
        return not self.request.user.groups.filter(name="banned users").exists()

    def handle_no_permission(self) -> HttpResponseRedirect:
        """
        Redirect to index with warning message if authenticated, otherwise to login.
        """
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.warning(self.request, "You have been banned from creating listings.")
        return HttpResponseRedirect(reverse("index"))
