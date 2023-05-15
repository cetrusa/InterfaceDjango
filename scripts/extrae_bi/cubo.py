import os, sys
import pandas as pd
from os import path, system
from time import time
from distutils.log import error
from sqlalchemy.sql import text
import sqlalchemy
import pymysql
import csv
import zipfile
from zipfile import ZipFile
from django.http import HttpResponse, FileResponse, JsonResponse
from scripts.StaticPage import StaticPage
from scripts.conexion import Conexion
from scripts.config import ConfigBasic

####################################################################
import logging

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    filemode="w",
)
####################################################################
logging.info("Inciando Proceso")


class Cubo_Ventas:
    StaticPage = StaticPage()

    def __init__(self, database_name, IdtReporteIni, IdtReporteFin):
        ConfigBasic(database_name)
        StaticPage.IdtReporteIni = IdtReporteIni
        StaticPage.IdtReporteFin = IdtReporteFin

    def Procedimiento_a_Excel():
        a = StaticPage.dbBi
        IdDs = ""
        compra = 0
        consig = 0
        nd = 0
        sql = StaticPage.nmProcedureExcel
        StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{StaticPage.IdtReporteIni}_a_{StaticPage.IdtReporteFin}.xlsx"
        StaticPage.file_path = os.path.join("media", StaticPage.archivo_cubo_ventas)
        if StaticPage.txProcedureExcel:
            with pd.ExcelWriter(StaticPage.file_path, engine="openpyxl") as writer:
                for hoja in StaticPage.txProcedureExcel:
                    if a == "powerbi_tym_eje":
                        sqlout = text(
                            f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}','{compra}','{consig}','{nd}');"
                        )
                    else:
                        sqlout = text(
                            f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}');"
                        )
                    try:
                        with StaticPage.conin2.connect() as connectionout:
                            cursor = connectionout.execution_options(
                                isolation_level="READ COMMITTED"
                            )
                            resultado = pd.read_sql_query(sql=sqlout, con=cursor)
                            resultado.to_excel(
                                writer, index=False, sheet_name=hoja, header=True
                            )
                            writer.sheets[hoja].sheet_state = "visible"
                    except Exception as e:
                        print(
                            logging.info(
                                f"No fue posible generar la información por {e}"
                            )
                        )
        else:
            return JsonResponse(
                {
                    "success": True,
                    "error_message": f"La empresa {StaticPage.nmEmpresa} no maneja cubo",
                }
            )
