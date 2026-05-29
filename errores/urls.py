from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'errores'


def login_path(route, view, kwargs=None, name=None):
    return path(route, login_required(view), kwargs, name)

urlpatterns = [
    login_path('', views.lista_errores, name='lista'),
    login_path('error/nuevo/', views.crear_error, name='crear'),
    login_path('error/<int:pk>/', views.detalle_error, name='detalle'),
    login_path('error/<int:pk>/editar/', views.editar_error, name='editar'),
    login_path('error/<int:pk>/eliminar/', views.eliminar_error, name='eliminar'),
    login_path('plataforma/hardware/', views.lista_hardware, name='hardware_lista'),
    login_path('plataforma/hardware/nuevo/', views.crear_hardware, name='hardware_crear'),
    login_path('plataforma/hardware/<int:pk>/editar/', views.editar_hardware, name='hardware_editar'),
    login_path('plataforma/hardware/<int:pk>/eliminar/', views.eliminar_hardware, name='hardware_eliminar'),
    login_path('plataforma/sistemas/', views.lista_sistemas, name='sistema_lista'),
    login_path('plataforma/sistemas/nuevo/', views.crear_sistema, name='sistema_crear'),
    login_path('plataforma/sistemas/<int:pk>/editar/', views.editar_sistema, name='sistema_editar'),
    login_path('plataforma/sistemas/<int:pk>/eliminar/', views.eliminar_sistema, name='sistema_eliminar'),
    login_path('responsables/', views.lista_responsables, name='responsable_lista'),
    login_path('responsables/nuevo/', views.crear_responsable, name='responsable_crear'),
    login_path('responsables/<int:pk>/editar/', views.editar_responsable, name='responsable_editar'),
    login_path('responsables/<int:pk>/eliminar/', views.eliminar_responsable, name='responsable_eliminar'),
    login_path('departamentos/', views.lista_departamentos, name='departamento_lista'),
    login_path('departamentos/nuevo/', views.crear_departamento, name='departamento_crear'),
    login_path('departamentos/<int:pk>/', views.detalle_departamento, name='departamento_detalle'),
    login_path('departamentos/<int:pk>/editar/', views.editar_departamento, name='departamento_editar'),
    login_path('departamentos/<int:pk>/eliminar/', views.eliminar_departamento, name='departamento_eliminar'),
    login_path('departamentos/<int:departamento_pk>/responsables/nuevo/', views.crear_responsable_departamento, name='departamento_responsable_crear'),
    login_path('departamentos/<int:departamento_pk>/responsables/<int:pk>/editar/', views.editar_responsable_departamento, name='departamento_responsable_editar'),
    login_path('departamentos/<int:departamento_pk>/responsables/<int:pk>/eliminar/', views.eliminar_responsable_departamento, name='departamento_responsable_eliminar'),
    login_path('pruebas/', views.lista_pruebas, name='prueba_lista'),
    login_path('pruebas/nuevo/', views.crear_prueba, name='prueba_crear'),
    login_path('pruebas/<int:pk>/editar/', views.editar_prueba, name='prueba_editar'),
    login_path('pruebas/<int:pk>/eliminar/', views.eliminar_prueba, name='prueba_eliminar'),
    login_path('soluciones/', views.lista_soluciones, name='solucion_lista'),
    login_path('soluciones/nuevo/', views.crear_solucion, name='solucion_crear'),
    login_path('soluciones/rapida/', views.crear_solucion_rapida, name='solucion_crear_rapida'),
    login_path('soluciones/<int:pk>/rapida/', views.editar_solucion_rapida, name='solucion_editar_rapida'),
    login_path('soluciones/<int:pk>/editar/', views.editar_solucion, name='solucion_editar'),
    login_path('soluciones/<int:pk>/eliminar/', views.eliminar_solucion, name='solucion_eliminar'),
]
