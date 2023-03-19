
import os,sys
# from unipath import Path
import pandas as pd
from os import path, system
from distutils.log import error
import ast
import mariadb
from sqlalchemy.sql import text
import sqlalchemy
import pymysql
from scripts.StaticPage import StaticPage
from scripts.conexion import Conexion
from scripts.config import ConfigBasic
import time
import csv
import zipfile
from zipfile import ZipFile
from django.http import HttpResponse,FileResponse,JsonResponse
from io import BytesIO

####################################################################
import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s", filemode="w")
####################################################################
logging.info('Inciando Proceso')

class Interface_Contable:
    StaticPage = StaticPage()
    def __init__(self,database_name,IdtReporteIni, IdtReporteFin):
        ConfigBasic(database_name)
        StaticPage.IdtReporteIni=IdtReporteIni
        StaticPage.IdtReporteFin=IdtReporteFin

    def Procedimiento_a_Excel(self):
        a = StaticPage.dbBi
        IdDs = ''
        compra = 0
        consig = 0
        nd = 0
        sql = StaticPage.nmProcedureInterface
        StaticPage.archivo_cubo_ventas = f"Interface_Contable_{StaticPage.nmCarpeta}_de_{StaticPage.IdtReporteIni}_a_{StaticPage.IdtReporteFin}.xlsx"
        StaticPage.file_path = os.path.join('media', StaticPage.archivo_cubo_ventas)
        if StaticPage.txProcedureInterface:    
            with pd.ExcelWriter( StaticPage.file_path, engine='openpyxl') as writer:
                for hoja in StaticPage.txProcedureInterface:
                    if a == 'powerbi_tym_eje':
                        sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}','{compra}','{consig}','{nd}');")     
                    else:
                        sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{hoja}');")
                    with StaticPage.conin2.connect() as connectionout:
                        cursor = connectionout.execution_options(isolation_level="READ COMMITTED")
                        resultado = pd.read_sql_query(sql=sqlout, con=cursor)
                        resultado.to_excel(writer, index=False, sheet_name=hoja, header=True)
                        writer.sheets[hoja].sheet_state = 'visible'
        else:
            return JsonResponse({'success': True, 'error_message': f'La empresa {StaticPage.nmEmpresa} no maneja interface contable'})
                    
    def Procedimiento_a_Plano(self):
        a = StaticPage.dbBi
        IdDs = ''
        sql = StaticPage.nmProcedureCsv
        sql2 = StaticPage.nmProcedureCsv2
        StaticPage.archivo_plano = f"Plano_{StaticPage.nmCarpeta}_de_{StaticPage.IdtReporteIni}_a_{StaticPage.IdtReporteFin}.zip"
        StaticPage.file_path = os.path.join('media', StaticPage.archivo_plano)
        if StaticPage.txProcedureCsv:
            with zipfile.ZipFile(StaticPage.file_path, "w") as zf:
                for a in StaticPage.txProcedureCsv:
                    print("aqui toy")
                    with zf.open(a+'.txt', "w") as buffer:
                        sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{a}');")
                        with StaticPage.conin2.connect() as connectionout:
                            cursor = connectionout.execution_options(isolation_level="READ COMMITTED")
                            resultado = pd.read_sql_query(sql=sqlout, con=cursor)
                            resultado.to_csv(buffer,sep='|',index=False,float_format='%.2f',header=True)
                            # time.sleep(1)
        elif StaticPage.txProcedureCsv2:    
            with zipfile.ZipFile(StaticPage.file_path, "w") as zf:
                for a in StaticPage.txProcedureCsv2:
                    with zf.open(a+'.txt', "w") as buffer:
                        sqlout = text(f"CALL {sql}('{StaticPage.IdtReporteIni}','{StaticPage.IdtReporteFin}','{IdDs}','{a}');")
                        with StaticPage.conin2.connect() as connectionout:
                            cursor = connectionout.execution_options(isolation_level="READ COMMITTED")
                            resultado = pd.read_sql_query(sql=sqlout, con=cursor)
                            resultado.to_csv(buffer,sep=',',index=False,header=False,float_format='%.0f')
                            # time.sleep(1)
        else:
            return JsonResponse({'success': True, 'error_message': f'La empresa {StaticPage.nmEmpresa} no maneja interface contable'})