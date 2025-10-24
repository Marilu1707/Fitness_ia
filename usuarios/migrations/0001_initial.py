# Generated manually to bootstrap the usuarios app schema.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edad', models.PositiveIntegerField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=4)),
                ('nivel', models.CharField(choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')], max_length=10)),
                ('dias_entrenamiento', models.PositiveIntegerField(default=3)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('ubicacion', models.CharField(max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='profesionales/')),
                ('tipo', models.CharField(choices=[('entrenador', 'Entrenador'), ('nutricionista', 'Nutricionista')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('peso_deseado', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('dias_entrenamiento', models.IntegerField(default=3)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='progreso/')),
                ('peso_actual', models.FloatField(blank=True, null=True)),
                ('horas', models.FloatField(default=0)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha', '-id'],
            },
        ),
    ]
