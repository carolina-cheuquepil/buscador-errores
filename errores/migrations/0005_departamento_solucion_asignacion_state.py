from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('errores', '0004_sistema_descripcion_state'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Departamento',
                    fields=[
                        ('id', models.AutoField(db_column='departamento_id', primary_key=True, serialize=False)),
                        ('nombre', models.CharField(max_length=100, unique=True)),
                        ('activo', models.BooleanField(default=True)),
                    ],
                    options={
                        'verbose_name': 'Departamento',
                        'verbose_name_plural': 'Departamentos',
                        'db_table': 'departamento',
                        'ordering': ['nombre'],
                    },
                ),
                migrations.AddField(
                    model_name='responsable',
                    name='departamento',
                    field=models.ForeignKey(
                        blank=True,
                        db_column='departamento_id',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='responsables',
                        to='errores.departamento',
                    ),
                ),
                migrations.RemoveField(
                    model_name='error',
                    name='solucion',
                ),
                migrations.DeleteModel(
                    name='SolucionResponsable',
                ),
                migrations.CreateModel(
                    name='SolucionAsignacion',
                    fields=[
                        ('id', models.AutoField(db_column='solucion_asignacion_id', primary_key=True, serialize=False)),
                        ('rol', models.CharField(blank=True, max_length=100, null=True)),
                        ('principal', models.BooleanField(default=False)),
                        ('activo', models.BooleanField(default=True)),
                        (
                            'departamento',
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.CASCADE,
                                to='errores.departamento',
                            ),
                        ),
                        (
                            'responsable',
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.CASCADE,
                                to='errores.responsable',
                            ),
                        ),
                        (
                            'solucion',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name='asignaciones',
                                to='errores.solucion',
                            ),
                        ),
                    ],
                    options={
                        'verbose_name': 'Asignacion de solucion',
                        'verbose_name_plural': 'Asignaciones de soluciones',
                        'db_table': 'solucion_asignacion',
                        'ordering': ['-principal', 'responsable__nombre', 'departamento__nombre'],
                    },
                ),
            ],
        ),
    ]
