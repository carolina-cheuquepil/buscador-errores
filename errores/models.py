from .dominios.catalogos.models import Frecuencia, Prueba
from .dominios.errores.models import Error, ErrorPrueba, ErrorSolucion
from .dominios.plataforma.models import Hardware, HardwareSistema, Modulo, Sistema
from .dominios.soluciones.models import Departamento, DepartamentoContacto, Responsable, Solucion, SolucionAsignacion

__all__ = [
    'Departamento',
    'DepartamentoContacto',
    'Error',
    'ErrorPrueba',
    'ErrorSolucion',
    'Frecuencia',
    'Hardware',
    'HardwareSistema',
    'Modulo',
    'Prueba',
    'Responsable',
    'Sistema',
    'Solucion',
    'SolucionAsignacion',
]
