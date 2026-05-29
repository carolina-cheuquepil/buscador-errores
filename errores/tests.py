from django.test import TestCase
from django.urls import resolve, reverse


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
