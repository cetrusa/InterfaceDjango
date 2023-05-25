from celery import shared_task
from scripts.extrae_bi.cubo import Cubo_Ventas
from scripts.StaticPage import StaticPage
import logging

@shared_task
def cubo_ventas_task(database_name, IdtReporteIni, IdtReporteFin):
    try:
        cubo_ventas = Cubo_Ventas(database_name, IdtReporteIni, IdtReporteFin)
        cubo_ventas.Procedimiento_a_Excel()
        file_path = StaticPage.file_path
        file_name = StaticPage.archivo_cubo_ventas
        return {'file_path': file_path, 'file_name': file_name}
    except Exception as e:
        logging.exception("Error al ejecutar cubo_ventas_task")
        raise
