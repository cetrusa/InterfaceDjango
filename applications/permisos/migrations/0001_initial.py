# Generated by Django 4.1.5 on 2023-03-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PermisosBarra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('nav_bar', 'Ver la barra de menú'), ('cubo', 'Generar cubo de ventas'), ('interface', 'Generar interface contable'), ('plano', 'Generar archivo plano'), ('informe_bi', 'Informe Bi'), ('actualizar_base', 'Actualzación de datos'), ('actualizacion_bi', 'Actualizar Bi'), ('nuevo', 'nueva opción')),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ConfDt',
            fields=[
                ('nbDt', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nmDt', models.CharField(blank=True, max_length=100, null=True)),
                ('txDtIni', models.TextField(blank=True, null=True)),
                ('txDtFin', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'conf_dt',
            },
        ),
        migrations.CreateModel(
            name='ConfEmpresas',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nmEmpresa', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('nbServerSidis', models.BigIntegerField(blank=True, null=True)),
                ('dbSidis', models.CharField(blank=True, max_length=150, null=True)),
                ('nbServerBi', models.BigIntegerField(blank=True, null=True)),
                ('dbBi', models.CharField(blank=True, max_length=150, null=True)),
                ('txProcedureExtrae', models.CharField(blank=True, max_length=100, null=True)),
                ('txProcedureCargue', models.TextField(blank=True, null=True)),
                ('nmProcedureInterface', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureInterface', models.TextField(blank=True, null=True)),
                ('nmProcedureExcel', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureExcel', models.TextField(blank=True, null=True)),
                ('nmProcedureExcel2', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureExcel2', models.TextField(blank=True, null=True)),
                ('nmProcedureCsv', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureCsv', models.TextField(blank=True, null=True)),
                ('nmProcedureCsv2', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureCsv2', models.TextField(blank=True, null=True)),
                ('nmProcedureSql', models.CharField(blank=True, max_length=30, null=True)),
                ('txProcedureSql', models.TextField(blank=True, null=True)),
                ('report_id_powerbi', models.CharField(blank=True, max_length=255, null=True)),
                ('dataset_id_powerbi', models.CharField(blank=True, max_length=255, null=True)),
                ('url_powerbi', models.TextField(blank=True, null=True)),
                ('estado', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'conf_empresas',
            },
        ),
        migrations.CreateModel(
            name='ConfServer',
            fields=[
                ('nbServer', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nmServer', models.CharField(blank=True, max_length=30, null=True)),
                ('hostServer', models.CharField(blank=True, max_length=100, null=True)),
                ('portServer', models.CharField(blank=True, max_length=10, null=True)),
                ('nbTipo', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'conf_server',
            },
        ),
        migrations.CreateModel(
            name='ConfSql',
            fields=[
                ('nbSql', models.BigIntegerField(primary_key=True, serialize=False)),
                ('txSql', models.TextField(blank=True, null=True)),
                ('nmReporte', models.CharField(blank=True, max_length=100, null=True)),
                ('txTabla', models.CharField(blank=True, max_length=100, null=True)),
                ('txDescripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('nmProcedure_out', models.CharField(blank=True, max_length=100, null=True)),
                ('nmProcedure_in', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'conf_sql',
            },
        ),
        migrations.CreateModel(
            name='ConfTipo',
            fields=[
                ('nbTipo', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nmUsr', models.CharField(blank=True, max_length=50, null=True)),
                ('txPass', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'conf_tipo',
            },
        ),
    ]
