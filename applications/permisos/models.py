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
        
