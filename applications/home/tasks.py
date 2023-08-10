from scripts.extrae_bi.cubo import Cubo_Ventas
from scripts.extrae_bi.interface import Interface_Contable
from scripts.extrae_bi.extrae_bi import Extrae_Bi
from scripts.StaticPage import StaticPage
import logging

# from celery import shared_task
# @shared_task

from django_rq import job

@job
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
    
@job
def interface_task(database_name, IdtReporteIni, IdtReporteFin):
    try:
        interface_contable = Interface_Contable(database_name, IdtReporteIni, IdtReporteFin)
        interface_contable.Procedimiento_a_Excel()
        file_path = StaticPage.file_path
        file_name = StaticPage.archivo_plano
        return {'file_path': file_path, 'file_name': file_name}
    except Exception as e:
        logging.exception("Error al ejecutar interface_contable_task")
        raise
    
    
@job
def plano_task(database_name, IdtReporteIni, IdtReporteFin):
    try:
        interface_plano = Interface_Contable(database_name, IdtReporteIni, IdtReporteFin)
        interface_plano.Procedimiento_a_Plano()
        file_path = StaticPage.file_path
        file_name = StaticPage.archivo_plano
        return {'file_path': file_path, 'file_name': file_name}
    except Exception as e:
        logging.exception("Error al ejecutar interface_plano_task")
        raise
    
@job
def extrae_bi_task(database_name):
    try:
        extrae_data = Extrae_Bi(database_name)
        extrae_data.extractor()
        file_path = StaticPage.file_path
        file_name = StaticPage.archivo_plano
        return {'file_path': file_path, 'file_name': file_name}
    except Exception as e:
        logging.exception("Error al ejecutar interface_plano_task")
        raise