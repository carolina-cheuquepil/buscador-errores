from django.core.exceptions import ValidationError
from django.db import models


class Error(models.Model):
    id = models.AutoField(primary_key=True, db_column='error_id')
    descripcion = models.TextField('Descripcion', db_column='error_descripcion')
    imagen_error = models.TextField('Imagen del error', blank=True, db_column='error_imagen')
    usuario = models.TextField('Usuario', blank=True, db_column='usuario_contexto')
    hardware = models.ForeignKey(
        'Hardware', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='errores',
    )
    sistema = models.ForeignKey(
        'Sistema', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='errores',
    )
    modulo = models.ForeignKey(
        'Modulo', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='errores',
    )
    causa = models.TextField('Causa del problema', blank=True, db_column='causa_problema')
    frecuencia = models.ForeignKey(
        'Frecuencia', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='errores',
    )
    comentarios = models.TextField('Comentarios', blank=True)
    soluciones = models.ManyToManyField(
        'Solucion',
        through='ErrorSolucion',
        related_name='errores_asociados',
        blank=True,
    )
    pruebas = models.ManyToManyField(
        'Prueba',
        through='ErrorPrueba',
        related_name='errores',
        blank=True,
    )

    creado = models.DateTimeField(auto_now_add=True, db_column='creado_en')
    actualizado = models.DateTimeField(auto_now=True, db_column='actualizado_en')

    class Meta:
        db_table = 'error'
        verbose_name = 'Error'
        verbose_name_plural = 'Errores'
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(modulo__isnull=True) | models.Q(sistema__isnull=False),
                name='ck_error_modulo_requiere_sistema',
            ),
        ]

    def __str__(self):
        texto = (self.descripcion or '').strip().replace('\n', ' ')
        return f'#{self.id} - {texto[:80]}'

    def clean(self):
        super().clean()
        if self.modulo_id and not self.sistema_id:
            raise ValidationError({'sistema': 'Debe indicar un sistema si selecciona un modulo.'})
        if self.modulo_id and self.sistema_id and self.modulo.sistema_id != self.sistema_id:
            raise ValidationError({'modulo': 'El modulo debe pertenecer al sistema seleccionado.'})


class ErrorSolucion(models.Model):
    pk = models.CompositePrimaryKey('error', 'solucion')
    error = models.ForeignKey('Error', on_delete=models.CASCADE)
    solucion = models.ForeignKey('Solucion', on_delete=models.CASCADE)
    orden = models.IntegerField(default=1)
    notas = models.TextField(blank=True)

    class Meta:
        db_table = 'error_solucion'
        verbose_name = 'Error / solucion'
        verbose_name_plural = 'Errores / soluciones'
        ordering = ['error_id', 'orden']

    def __str__(self):
        return f'{self.error} - {self.solucion}'


class ErrorPrueba(models.Model):
    pk = models.CompositePrimaryKey('error', 'prueba')
    error = models.ForeignKey('Error', on_delete=models.CASCADE)
    prueba = models.ForeignKey('Prueba', on_delete=models.CASCADE, db_column='prueba_tipica_id')
    resultado_esperado = models.TextField(blank=True)

    class Meta:
        db_table = 'error_prueba'
        verbose_name = 'Error / prueba'
        verbose_name_plural = 'Errores / pruebas'

    def __str__(self):
        return f'{self.error} - {self.prueba}'
