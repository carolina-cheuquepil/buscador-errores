from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from django.urls.resolvers import URLPattern

from .urls import urlpatterns


class LoginRequiredTests(TestCase):
    def test_lista_redirects_to_login_without_session(self):
        response = self.client.get(reverse('errores:lista'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('errores:lista')}",
        )

    def test_lista_url_is_wrapped_with_login_required(self):
        callback = resolve(reverse('errores:lista')).func

        self.assertTrue(hasattr(callback, 'login_url'))
        self.assertEqual(callback.redirect_field_name, 'next')

    def test_all_app_urls_are_wrapped_with_login_required(self):
        for pattern in urlpatterns:
            with self.subTest(route=str(pattern.pattern), name=pattern.name):
                self.assertIsInstance(pattern, URLPattern)
                self.assertTrue(hasattr(pattern.callback, 'login_url'))
                self.assertEqual(pattern.callback.redirect_field_name, 'next')

    def test_authenticated_user_without_view_permission_gets_forbidden(self):
        user = get_user_model().objects.create_user(
            username='sin_permiso',
            password='clave-segura-123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('errores:lista'))

        self.assertEqual(response.status_code, 403)
