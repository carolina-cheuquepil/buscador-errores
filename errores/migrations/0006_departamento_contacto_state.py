from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('errores', '0005_departamento_solucion_asignacion_state'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='DepartamentoContacto',
                    fields=[
                        ('id', models.AutoField(db_column='contacto_id', primary_key=True, serialize=False)),
                        ('tipo', models.CharField(max_length=50)),
                        ('numero', models.CharField(max_length=50)),
                        ('activo', models.BooleanField(default=True)),
                        (
                            'departamento',
                            models.ForeignKey(
                                db_column='departamento_id',
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name='contactos',
                                to='errores.departamento',
                            ),
                        ),
                    ],
                    options={
                        'verbose_name': 'Contacto de departamento',
                        'verbose_name_plural': 'Contactos de departamentos',
                        'db_table': 'departamento_contacto',
                        'ordering': ['tipo', 'numero'],
                    },
                ),
            ],
        ),
    ]
