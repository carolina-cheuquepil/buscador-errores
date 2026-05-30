from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

app_name = 'errores'


def secure_path(route, view, permission, kwargs=None, name=None):
    protected_view = login_required(permission_required(
        permission,
        raise_exception=True,
    )(view))
    return path(route, protected_view, kwargs, name)


urlpatterns = [
    secure_path('', views.lista_errores, 'errores.view_error', name='lista'),
    secure_path('error/nuevo/', views.crear_error, 'errores.add_error', name='crear'),
    secure_path('error/<int:pk>/', views.detalle_error, 'errores.view_error', name='detalle'),
    secure_path('error/<int:pk>/editar/', views.editar_error, 'errores.change_error', name='editar'),
    secure_path('error/<int:pk>/eliminar/', views.eliminar_error, 'errores.delete_error', name='eliminar'),
    secure_path('plataforma/hardware/', views.lista_hardware, 'errores.view_hardware', name='hardware_lista'),
    secure_path('plataforma/hardware/nuevo/', views.crear_hardware, 'errores.add_hardware', name='hardware_crear'),
    secure_path('plataforma/hardware/<int:pk>/editar/', views.editar_hardware, 'errores.change_hardware', name='hardware_editar'),
    secure_path('plataforma/hardware/<int:pk>/eliminar/', views.eliminar_hardware, 'errores.delete_hardware', name='hardware_eliminar'),
    secure_path('plataforma/sistemas/', views.lista_sistemas, 'errores.view_sistema', name='sistema_lista'),
    secure_path('plataforma/sistemas/nuevo/', views.crear_sistema, 'errores.add_sistema', name='sistema_crear'),
    secure_path('plataforma/sistemas/<int:pk>/editar/', views.editar_sistema, 'errores.change_sistema', name='sistema_editar'),
    secure_path('plataforma/sistemas/<int:pk>/eliminar/', views.eliminar_sistema, 'errores.delete_sistema', name='sistema_eliminar'),
    secure_path('responsables/', views.lista_responsables, 'errores.view_responsable', name='responsable_lista'),
    secure_path('responsables/nuevo/', views.crear_responsable, 'errores.add_responsable', name='responsable_crear'),
    secure_path('responsables/<int:pk>/editar/', views.editar_responsable, 'errores.change_responsable', name='responsable_editar'),
    secure_path('responsables/<int:pk>/eliminar/', views.eliminar_responsable, 'errores.delete_responsable', name='responsable_eliminar'),
    secure_path('departamentos/', views.lista_departamentos, 'errores.view_departamento', name='departamento_lista'),
    secure_path('departamentos/nuevo/', views.crear_departamento, 'errores.add_departamento', name='departamento_crear'),
    secure_path('departamentos/<int:pk>/', views.detalle_departamento, 'errores.view_departamento', name='departamento_detalle'),
    secure_path('departamentos/<int:pk>/editar/', views.editar_departamento, 'errores.change_departamento', name='departamento_editar'),
    secure_path('departamentos/<int:pk>/eliminar/', views.eliminar_departamento, 'errores.delete_departamento', name='departamento_eliminar'),
    secure_path('departamentos/<int:departamento_pk>/responsables/nuevo/', views.crear_responsable_departamento, 'errores.add_responsable', name='departamento_responsable_crear'),
    secure_path('departamentos/<int:departamento_pk>/responsables/<int:pk>/editar/', views.editar_responsable_departamento, 'errores.change_responsable', name='departamento_responsable_editar'),
    secure_path('departamentos/<int:departamento_pk>/responsables/<int:pk>/eliminar/', views.eliminar_responsable_departamento, 'errores.delete_responsable', name='departamento_responsable_eliminar'),
    secure_path('pruebas/', views.lista_pruebas, 'errores.view_prueba', name='prueba_lista'),
    secure_path('pruebas/nuevo/', views.crear_prueba, 'errores.add_prueba', name='prueba_crear'),
    secure_path('pruebas/<int:pk>/editar/', views.editar_prueba, 'errores.change_prueba', name='prueba_editar'),
    secure_path('pruebas/<int:pk>/eliminar/', views.eliminar_prueba, 'errores.delete_prueba', name='prueba_eliminar'),
    secure_path('soluciones/', views.lista_soluciones, 'errores.view_solucion', name='solucion_lista'),
    secure_path('soluciones/nuevo/', views.crear_solucion, 'errores.add_solucion', name='solucion_crear'),
    secure_path('soluciones/rapida/', views.crear_solucion_rapida, 'errores.add_solucion', name='solucion_crear_rapida'),
    secure_path('soluciones/<int:pk>/rapida/', views.editar_solucion_rapida, 'errores.change_solucion', name='solucion_editar_rapida'),
    secure_path('soluciones/<int:pk>/editar/', views.editar_solucion, 'errores.change_solucion', name='solucion_editar'),
    secure_path('soluciones/<int:pk>/eliminar/', views.eliminar_solucion, 'errores.delete_solucion', name='solucion_eliminar'),
]
