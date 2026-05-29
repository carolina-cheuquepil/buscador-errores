from django.db import models


class Solucion(models.Model):
    id = models.AutoField(primary_key=True, db_column='solucion_id')
    nombre = models.CharField('Titulo', max_length=220, unique=True, db_column='titulo')
    pasos = models.TextField(blank=True)
    anexos = models.TextField(blank=True)

    class Meta:
        db_table = 'solucion'
        verbose_name = 'Solucion'
        verbose_name_plural = 'Soluciones'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='departamento_id')
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class DepartamentoContacto(models.Model):
    id = models.AutoField(primary_key=True, db_column='contacto_id')
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        db_column='departamento_id',
        related_name='contactos',
    )
    tipo = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'departamento_contacto'
        verbose_name = 'Contacto de departamento'
        verbose_name_plural = 'Contactos de departamentos'
        ordering = ['tipo', 'numero']

    def __str__(self):
        return f'{self.departamento} - {self.tipo}: {self.numero}'


class Responsable(models.Model):
    id = models.AutoField(primary_key=True, db_column='responsable_id')
    nombre = models.CharField(max_length=160, unique=True, db_column='responsable_nombre')
    cargo = models.CharField(max_length=120, blank=True)
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='departamento_id',
        related_name='responsables',
    )
    contacto = models.CharField(max_length=160, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'responsable'
        verbose_name = 'Responsable'
        verbose_name_plural = 'Responsables'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class SolucionAsignacion(models.Model):
    id = models.AutoField(primary_key=True, db_column='solucion_asignacion_id')
    solucion = models.ForeignKey('Solucion', on_delete=models.CASCADE, related_name='asignaciones')
    responsable = models.ForeignKey('Responsable', on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, null=True, blank=True)
    rol = models.CharField(max_length=100, blank=True, null=True)
    principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'solucion_asignacion'
        verbose_name = 'Asignacion de solucion'
        verbose_name_plural = 'Asignaciones de soluciones'
        ordering = ['-principal', 'responsable__nombre', 'departamento__nombre']

    def __str__(self):
        asignado = self.responsable or self.departamento
        return f'{self.solucion} - {asignado}'
