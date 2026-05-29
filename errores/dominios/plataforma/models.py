from django.db import models


class Hardware(models.Model):
    id = models.AutoField(primary_key=True, db_column='hardware_id')
    nombre = models.CharField(max_length=120, unique=True, db_column='hardware')
    so = models.CharField('Sistema operativo', max_length=160, blank=True, db_column='sistema_operativo')
    sistemas = models.ManyToManyField(
        'Sistema',
        through='HardwareSistema',
        related_name='hardware',
        blank=True,
    )

    class Meta:
        db_table = 'hardware'
        verbose_name = 'Hardware'
        verbose_name_plural = 'Hardware'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Sistema(models.Model):
    id = models.AutoField(primary_key=True, db_column='sistema_id')
    nombre = models.CharField(max_length=160, unique=True, db_column='sistema_nombre')
    descripcion = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'sistema'
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Modulo(models.Model):
    id = models.AutoField(primary_key=True, db_column='modulo_id')
    nombre = models.CharField('Modulo', max_length=180, db_column='modulo_nombre')
    sistema = models.ForeignKey('Sistema', on_delete=models.CASCADE, related_name='modulos')

    class Meta:
        db_table = 'modulo'
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        ordering = ['sistema__nombre', 'nombre']
        constraints = [
            models.UniqueConstraint(fields=['sistema', 'id'], name='uq_modulo_sistema_id'),
            models.UniqueConstraint(fields=['sistema', 'nombre'], name='uq_modulo_sistema_nombre'),
        ]

    def __str__(self):
        return f'{self.sistema} - {self.nombre}'


class HardwareSistema(models.Model):
    pk = models.CompositePrimaryKey('hardware', 'sistema')
    hardware = models.ForeignKey('Hardware', on_delete=models.CASCADE)
    sistema = models.ForeignKey('Sistema', on_delete=models.CASCADE)

    class Meta:
        db_table = 'hardware_sistema'
        verbose_name = 'Hardware / sistema'
        verbose_name_plural = 'Hardware / sistemas'

    def __str__(self):
        return f'{self.hardware} - {self.sistema}'
