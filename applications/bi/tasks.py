from scripts.extrae_bi.apipowerbi import Api_PowerBi
from scripts.StaticPage import StaticPage
import logging

# from celery import shared_task
# @shared_task

from django_rq import job


@job('default', timeout=1800)
def actualiza_bi_task(database_name):
    try:
        # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
        ApiPBi = Api_PowerBi(database_name)
        # Ejecutamos el script aquí
        ApiPBi.run_datasetrefresh()
        file_path = StaticPage.file_path
        file_name = StaticPage.archivo_plano
        return {"file_path": file_path, "file_name": file_name}
    except Exception as e:
        logging.exception("Error al ejecutar interface_plano_task")
        raise
