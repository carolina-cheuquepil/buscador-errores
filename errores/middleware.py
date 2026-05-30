from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._requires_login(request):
            login_url = resolve_url(settings.LOGIN_URL)
            return redirect(f'{login_url}?next={request.get_full_path()}')
        return self.get_response(request)

    def _requires_login(self, request):
        if request.user.is_authenticated:
            return False

        path = request.path_info
        exempt_prefixes = tuple(filter(None, (
            resolve_url(settings.LOGIN_URL),
            reverse('logout'),
            '/admin/',
            self._path_prefix(settings.STATIC_URL),
            self._path_prefix(settings.MEDIA_URL),
        )))
        return not path.startswith(exempt_prefixes)

    def _path_prefix(self, url):
        if not url or '://' in url:
            return ''
        return url if url.startswith('/') else f'/{url}'
