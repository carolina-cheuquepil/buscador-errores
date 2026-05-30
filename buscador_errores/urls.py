from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from errores.auth_forms import SecureAuthenticationForm

login_view = LoginView.as_view(
    template_name='registration/login.html',
    authentication_form=SecureAuthenticationForm,
    redirect_authenticated_user=True,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('accounts/login/', login_view, name='accounts_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', include('errores.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
