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
import zipfile

# from pyspark.sql import SparkSession
import gzip
import tempfile
import sqlite3
from sqlalchemy import create_engine, text
from pandas.io.json import json_normalize
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell

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

    # Esta función funciona con hasta 300.000 registros
    # def Procedimiento_a_Excel_celery(self):
    #     a = StaticPage.dbBi
    #     IdDs = ""
    #     compra = 0
    #     consig = 0
    #     nd = 0
    #     sql = StaticPage.nmProcedureExcel
    #     StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{StaticPage.IdtReporteIni}_a_{StaticPage.IdtReporteFin}.xlsx"
    #     StaticPage.file_path = os.path.join("media", StaticPage.archivo_cubo_ventas)
    #     if StaticPage.txProcedureExcel:
    #         with pd.ExcelWriter(StaticPage.file_path, engine="openpyxl") as writer:
    #             for hoja in StaticPage.txProcedureExcel:
    #                 if a == "powerbi_tym_eje":
    #                     sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}','{compra}','{consig}','{nd}');")
    #                 else:
    #                     sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}');")
    #                 try:
    #                     with StaticPage.conin2.connect() as connectionout:
    #                         cursor = connectionout.execution_options(isolation_level="READ COMMITTED")
    #                         resultado = pd.read_sql_query(sql=sqlout, con=cursor)
    #                         resultado.to_excel(writer, index=False, sheet_name=hoja, header=True)
    #                         writer.sheets[hoja].sheet_state = "visible"
    #                 except Exception as e:
    #                     print(logging.info(f"No fue posible generar la información por {e}"))

    #     else:
    #         return JsonResponse({"success": True, "error_message": f"La empresa {StaticPage.nmEmpresa} no maneja cubo",})

    def Procedimiento_a_Excel(self):
        a = StaticPage.dbBi
        IdDs = ""
        compra = 0
        consig = 0
        nd = 0
        sql = StaticPage.nmProcedureExcel
        StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{StaticPage.IdtReporteIni}_a_{StaticPage.IdtReporteFin}"
        # Crea una conexión a una base de datos SQLite
        engine = create_engine("sqlite:///mydata.db")

        if StaticPage.txProcedureExcel:
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

                        # Use StaticPage.name para el nombre de la tabla
                        table_name = f"my_table_{StaticPage.name}_{hoja}"

                        # Dividir el DataFrame en fragmentos y escribir cada fragmento en la base de datos SQLite
                        chunksize = 50000  # tamaño del fragmento
                        for chunk in pd.read_sql_query(
                            sql=sqlout, con=cursor, chunksize=chunksize
                        ):
                            chunk.to_sql(
                                name=table_name,
                                con=engine,
                                if_exists="append",
                                index=False,
                            )

                        # Verificar el número total de registros
                        with engine.connect() as connection:
                            total_records = connection.execute(
                                f"SELECT COUNT(*) FROM {table_name}"
                            ).fetchone()[0]

                        if total_records > 1000000:
                            StaticPage.archivo_cubo_ventas = (
                                StaticPage.archivo_cubo_ventas + ".csv"
                            )
                            StaticPage.file_path = os.path.join(
                                "media", StaticPage.archivo_cubo_ventas
                            )
                            # Si los registros exceden 1000000, escribir en CSV
                            for chunk in pd.read_sql_query(
                                f"SELECT * FROM {table_name}",
                                engine,
                                chunksize=chunksize,
                            ):
                                chunk.to_csv(
                                    StaticPage.file_path, index=False, mode="a"
                                )
                        else:
                            StaticPage.archivo_cubo_ventas = (
                                StaticPage.archivo_cubo_ventas + ".xlsx"
                            )
                            StaticPage.file_path = os.path.join(
                                "media", StaticPage.archivo_cubo_ventas
                            )
                            # # Leer los datos de la base de datos SQLite en fragmentos y escribir cada fragmento en un archivo Excel
                            # with pd.ExcelWriter(StaticPage.file_path, engine="openpyxl") as writer:
                            #     for chunk in pd.read_sql_query(f"SELECT * FROM {table_name}", engine, chunksize=chunksize):
                            #         chunk.to_excel(writer, index=False, sheet_name=hoja, header=True)
                            #         writer.sheets[hoja].sheet_state = "visible"

                            # Crear un libro de trabajo en modo de solo escritura
                            wb = Workbook(write_only=True)
                            ws = wb.create_sheet()

                            for chunk in pd.read_sql_query(
                                f"SELECT * FROM {table_name}",
                                engine,
                                chunksize=chunksize,
                            ):
                                # Agregar las filas del DataFrame a la hoja de trabajo
                                for index, row in chunk.iterrows():
                                    cells = [
                                        WriteOnlyCell(ws, value=value) for value in row
                                    ]
                                    ws.append(cells)

                            # Guardar el libro de trabajo
                            wb.save(StaticPage.file_path)

                        # Eliminar la tabla una vez que los datos se han escrito en Excel
                        with engine.connect() as connection:
                            connection.execute(f"DROP TABLE {table_name}")

                except Exception as e:
                    print(
                        logging.info(f"No fue posible generar la información por {e}")
                    )

        else:
            return JsonResponse(
                {
                    "success": True,
                    "error_message": f"La empresa {StaticPage.nmEmpresa} no maneja cubo",
                }
            )
