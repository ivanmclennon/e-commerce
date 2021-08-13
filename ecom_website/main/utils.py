from allauth.account.adapter import DefaultAccountAdapter
from .models import Seller


class SellerAccountAdapter(DefaultAccountAdapter):
    """
    Allauth account adapter for Seller model
    """

    def new_user(self, request):
        """
        Returns Seller instance
        """
        return Seller()
