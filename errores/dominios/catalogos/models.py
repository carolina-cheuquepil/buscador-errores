from django.db import models


class Frecuencia(models.Model):
    id = models.AutoField(primary_key=True, db_column='frecuencia_id')
    nivel = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = 'frecuencia'
        verbose_name = 'Frecuencia'
        verbose_name_plural = 'Frecuencias'
        ordering = ['nivel']

    def __str__(self):
        return self.nivel


class Prueba(models.Model):
    id = models.AutoField(primary_key=True, db_column='prueba_tipica_id')
    descripcion = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'prueba'
        verbose_name = 'Prueba tipica'
        verbose_name_plural = 'Pruebas tipicas'
        ordering = ['descripcion']

    def __str__(self):
        return self.descripcion[:80]
