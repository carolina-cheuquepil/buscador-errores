from django.contrib import admin
from .dominios.catalogos import Frecuencia, Prueba
from .dominios.errores import Error, ErrorPrueba, ErrorSolucion
from .dominios.plataforma import Hardware, Modulo, Sistema
from .dominios.soluciones import Departamento, DepartamentoContacto, Responsable, Solucion, SolucionAsignacion


class ErrorSolucionInline(admin.TabularInline):
    model = ErrorSolucion
    extra = 1
    autocomplete_fields = ('solucion',)


class ErrorPruebaInline(admin.TabularInline):
    model = ErrorPrueba
    extra = 1
    autocomplete_fields = ('prueba',)


class SolucionAsignacionInline(admin.TabularInline):
    model = SolucionAsignacion
    extra = 1
    autocomplete_fields = ('responsable', 'departamento')


class DepartamentoContactoInline(admin.TabularInline):
    model = DepartamentoContacto
    extra = 1


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'so')
    search_fields = ('nombre', 'so')


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sistema')
    list_filter = ('sistema',)
    search_fields = ('nombre', 'sistema__nombre')
    autocomplete_fields = ('sistema',)


@admin.register(Frecuencia)
class FrecuenciaAdmin(admin.ModelAdmin):
    list_display = ('nivel',)
    search_fields = ('nivel',)


@admin.register(Solucion)
class SolucionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'pasos', 'anexos')
    inlines = (SolucionAsignacionInline,)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    inlines = (DepartamentoContactoInline,)


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'departamento', 'contacto', 'activo')
    list_filter = ('activo', 'departamento')
    search_fields = ('nombre', 'cargo', 'contacto', 'departamento__nombre')
    autocomplete_fields = ('departamento',)


@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('descripcion_corta',)
    search_fields = ('descripcion',)

    @admin.display(description='Descripcion')
    def descripcion_corta(self, obj):
        return (obj.descripcion or '')[:80]


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion_corta', 'hardware', 'sistema', 'modulo', 'frecuencia')
    list_filter = ('hardware', 'sistema', 'modulo', 'frecuencia')
    search_fields = ('descripcion', 'causa', 'soluciones__nombre', 'soluciones__pasos', 'comentarios', 'usuario')
    autocomplete_fields = ('hardware', 'sistema', 'modulo', 'frecuencia')
    inlines = (ErrorSolucionInline, ErrorPruebaInline)
    list_per_page = 30

    @admin.display(description='Descripción')
    def descripcion_corta(self, obj):
        return (obj.descripcion or '')[:80]
