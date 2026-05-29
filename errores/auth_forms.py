from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache


class SecureAuthenticationForm(AuthenticationForm):
    max_attempts = 5
    lockout_seconds = 15 * 60

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'current-password',
        })

    def clean(self):
        username = self.cleaned_data.get('username', '')
        cache_key = self._attempt_cache_key(username)
        attempts = cache.get(cache_key, 0)

        if attempts >= self.max_attempts:
            raise forms.ValidationError(
                'Demasiados intentos fallidos. Intenta nuevamente en 15 minutos.',
                code='too_many_login_attempts',
            )

        try:
            cleaned_data = super().clean()
        except forms.ValidationError:
            cache.set(cache_key, attempts + 1, self.lockout_seconds)
            raise

        cache.delete(cache_key)
        return cleaned_data

    def _attempt_cache_key(self, username):
        request = self.request
        remote_addr = ''
        if request is not None:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            if not remote_addr:
                remote_addr = request.META.get('REMOTE_ADDR', '')
        return f'login-attempts:{remote_addr}:{username.casefold()}'
