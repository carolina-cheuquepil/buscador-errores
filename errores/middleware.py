from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._requires_login(request):
            login_url = reverse('login')
            return redirect(f'{login_url}?next={request.get_full_path()}')
        return self.get_response(request)

    def _requires_login(self, request):
        if request.user.is_authenticated:
            return False

        path = request.path_info
        exempt_prefixes = (
            reverse('login'),
            reverse('logout'),
            '/admin/',
            settings.STATIC_URL,
            settings.MEDIA_URL,
        )
        return not path.startswith(exempt_prefixes)
