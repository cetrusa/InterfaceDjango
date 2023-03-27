from django.db import models

# Create your models here.
class PermisosBarra(models.Model):
    class Meta:
        managed = False
        permissions = (
            ('nav_bar', 'Ver la barra de menú'),
            ('cubo', 'Generar cubo de ventas'),
            ('interface', 'Generar interface contable'),
            ('plano', 'Generar archivo plano'),
            ('informe_bi', 'Informe Bi'),
            ('actualizar_base', 'Actualzación de datos'),
            ('actualizacion_bi', 'Actualizar Bi'),
            ('nuevo', 'nueva opción'),
        )
        
class ConfDt(models.Model):
    nbDt = models.BigIntegerField(primary_key=True)
    nmDt = models.CharField(max_length=100, null=True, blank=True)
    txDtIni = models.TextField(null=True, blank=True)
    txDtFin = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'conf_dt'
        # managed = False

class ConfEmpresas(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nmEmpresa = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    nbServerSidis = models.BigIntegerField(null=True, blank=True)
    dbSidis = models.CharField(max_length=150, null=True, blank=True)
    nbServerBi = models.BigIntegerField(null=True, blank=True)
    dbBi = models.CharField(max_length=150, null=True, blank=True)
    txProcedureExtrae = models.CharField(max_length=100, null=True, blank=True)
    txProcedureCargue = models.TextField(null=True, blank=True)
    nmProcedureInterface = models.CharField(max_length=30, null=True, blank=True)
    txProcedureInterface = models.TextField(null=True, blank=True)
    nmProcedureExcel = models.CharField(max_length=30, null=True, blank=True)
    txProcedureExcel = models.TextField(null=True, blank=True)
    nmProcedureExcel2 = models.CharField(max_length=30, null=True, blank=True)
    txProcedureExcel2 = models.TextField(null=True, blank=True)
    nmProcedureCsv = models.CharField(max_length=30, null=True, blank=True)
    txProcedureCsv = models.TextField(null=True, blank=True)
    nmProcedureCsv2 = models.CharField(max_length=30, null=True, blank=True)
    txProcedureCsv2 = models.TextField(null=True, blank=True)
    nmProcedureSql = models.CharField(max_length=30, null=True, blank=True)
    txProcedureSql = models.TextField(null=True, blank=True)
    report_id_powerbi = models.CharField(max_length=255, null=True, blank=True)
    dataset_id_powerbi = models.CharField(max_length=255, null=True, blank=True)
    url_powerbi = models.TextField(null=True, blank=True)
    estado = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'conf_empresas'
        # managed = False
        
    

class ConfServer(models.Model):
    nbServer = models.BigIntegerField(primary_key=True)
    nmServer = models.CharField(max_length=30, null=True, blank=True)
    hostServer = models.CharField(max_length=100, null=True, blank=True)
    portServer = models.CharField(max_length=10, null=True, blank=True)
    nbTipo = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'conf_server'
        # managed = False
        
        
class ConfSql(models.Model):
    nbSql = models.BigIntegerField(primary_key=True)
    txSql = models.TextField(null=True, blank=True)
    nmReporte = models.CharField(max_length=100, null=True, blank=True)
    txTabla = models.CharField(max_length=100, null=True, blank=True)
    txDescripcion = models.CharField(max_length=255, null=True, blank=True)
    nmProcedure_out = models.CharField(max_length=100, null=True, blank=True)
    nmProcedure_in = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'conf_sql'
        # managed = False

class ConfTipo(models.Model):
    nbTipo = models.BigIntegerField(primary_key=True)
    nmUsr = models.CharField(max_length=50, null=True, blank=True)
    txPass = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'conf_tipo'
        # managed = False

