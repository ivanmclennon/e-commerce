from django.shortcuts import render
from django.contrib import messages
from django.urls.base import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .forms import SubscriberForm


def subscribe_view(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed to newsletter!")
        else:
            messages.error(
                request, f"Cannot subscribe with email: {form.cleaned_data.email}"
            )
        return HttpResponseRedirect(reverse("index"))
    else:
        subscriber_form = SubscriberForm()
        return render(
            request,
            "subscribe.html",
            {
                "form": subscriber_form,
            },
        )
