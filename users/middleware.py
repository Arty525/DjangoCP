from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy


class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and hasattr(request.user, "is_banned")
            and request.user.is_banned
        ):
            logout(request)
            return redirect(reverse_lazy("users:login"))

        return self.get_response(request)
