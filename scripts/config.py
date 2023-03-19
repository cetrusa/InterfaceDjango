from scripts.StaticPage import StaticPage
from scripts.conexion import Conexion as con
import json
from django.core.exceptions import ImproperlyConfigured
import pandas as pd
import ast
import mariadb

####################################################################
import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s", filemode="w")
####################################################################
logging.info('Inciando Proceso')


class ConfigBasic():
    try:
        StaticPage = StaticPage()
        def __init__(self,database_name):
            StaticPage.nmCarpeta = str(database_name)
            
            # StaticPage.nmCarpeta = 'altimax'
            StaticPage.dir_actual = str('puente1dia')
            StaticPage.nmDt = StaticPage.dir_actual
            logging.info(StaticPage.nmCarpeta)
            logging.info(StaticPage.nmDt)

            StaticPage.con = con.ConexionMariadb()
            StaticPage.cursor = StaticPage.con.cursor(buffered = True,dictionary=True)
            sql = "SELECT * FROM powerbi_adm.conf_empresas WHERE nmCarpeta = %s;"
            StaticPage.cursor.execute(sql,(StaticPage.nmCarpeta,))
            resultado = StaticPage.cursor.fetchall()
            df = pd.DataFrame(resultado)
            StaticPage.nbEmpresa= df['nbEmpresa'].values[0]
            #logging.info(nbEmpresa)
            StaticPage.nmEmpresa=df['nmEmpresa'].values[0]
            logging.info(StaticPage.nmEmpresa)
            StaticPage.nmCarpeta=df['nmCarpeta'].values[0]
            StaticPage.nbServerSidis=df['nbServerSidis'].values[0]
            StaticPage.dbSidis=df['dbSidis'].values[0]
            StaticPage.nbServerBi=df['nbServerBi'].values[0]
            StaticPage.dbBi=df['dbBi'].values[0]
            StaticPage.txProcedureExtrae=ast.literal_eval(df['txProcedureExtrae'].values[0])
            StaticPage.txProcedureCargue=ast.literal_eval(df['txProcedureCargue'].values[0])
            StaticPage.nmProcedureExcel=df['nmProcedureExcel'].values[0]
            StaticPage.txProcedureExcel=ast.literal_eval(df['txProcedureExcel'].values[0])
            StaticPage.nmProcedureInterface=df['nmProcedureInterface'].values[0]
            StaticPage.txProcedureInterface=ast.literal_eval(df['txProcedureInterface'].values[0])
            StaticPage.nmProcedureExcel2=df['nmProcedureExcel2'].values[0]
            StaticPage.txProcedureExcel2=ast.literal_eval(df['txProcedureExcel2'].values[0])
            StaticPage.nmProcedureCsv=df['nmProcedureCsv'].values[0]
            StaticPage.txProcedureCsv=ast.literal_eval(df['txProcedureCsv'].values[0])
            StaticPage.nmProcedureCsv2=df['nmProcedureCsv2'].values[0]
            StaticPage.txProcedureCsv2=ast.literal_eval(df['txProcedureCsv2'].values[0])
            StaticPage.nmProcedureSql=df['nmProcedureSql'].values[0]
            StaticPage.txProcedureSql=ast.literal_eval(df['txProcedureSql'].values[0])
            StaticPage.report_id_powerbi=df['report_id_powerbi'].values[0]
            StaticPage.dataset_id_powerbi=df['dataset_id_powerbi'].values[0]
            StaticPage.url_powerbi=df['url_powerbi'].values[0]
            
            # Procedimientos para la extracción
            
            # Iniciamos a definir las fechas
            sql = "SELECT COUNT(*) FROM powerbi_adm.conf_dt WHERE nmDt = %s;"
            StaticPage.cursor.execute(sql,(StaticPage.nmDt,))
            count = StaticPage.cursor.fetchall()
            cdf = pd.DataFrame(count)
            count=cdf['COUNT(*)'].values[0]
            if count == [1]:
                sql ="SELECT * FROM powerbi_adm.conf_dt WHERE nmDt = %s;"
                StaticPage.cursor.execute(sql,(StaticPage.nmDt,))
                resultado2 = StaticPage.cursor.fetchall()
                df2 = pd.DataFrame(resultado2)
                StaticPage.txDtIni=str( df2['txDtIni'].values[0])
                StaticPage.txDtFin=str( df2['txDtFin'].values[0])
                StaticPage.cursor.execute(StaticPage.txDtIni)
                resultado3 = StaticPage.cursor.fetchall()
                df3 = pd.DataFrame(resultado3)
                StaticPage.IdtReporteIni=df3['IdtReporteIni'].values[0]
                
                StaticPage.cursor.execute(StaticPage.txDtFin)
                resultado4 = StaticPage.cursor.fetchall()
                df4 = pd.DataFrame(resultado4)
                StaticPage.IdtReporteFin=df4['IdtReporteFin'].values[0]
            else:
                sql ="SELECT * FROM powerbi_adm.conf_dt WHERE nmDt = %s;"
                StaticPage.cursor.execute(sql,('puente1dia',))
                resultado2 = StaticPage.cursor.fetchall()
                df2 = pd.DataFrame(resultado2)
                StaticPage.txDtIni=str( df2['txDtIni'].values[0])
                StaticPage.txDtFin=str( df2['txDtFin'].values[0])
                StaticPage.cursor.execute(StaticPage.txDtIni)
                resultado3 = StaticPage.cursor.fetchall()
                df3 = pd.DataFrame(resultado3)
                StaticPage.IdtReporteIni=df3['IdtReporteIni'].astype(str).values[0]
                
                StaticPage.cursor.execute(StaticPage.txDtFin)
                resultado4 = StaticPage.cursor.fetchall()
                df4 = pd.DataFrame(resultado4)
                StaticPage.IdtReporteFin=df4['IdtReporteFin'].astype(str).values[0]
            # Prepraramos datos de conexión
            sql = "SELECT * FROM powerbi_adm.conf_server WHERE nbServer = %s;"
            StaticPage.cursor.execute(sql,(StaticPage.nbServerSidis,))
            resultado5 = StaticPage.cursor.fetchall()
            df5 = pd.DataFrame(resultado5)
            StaticPage.hostServerOut=str(df5['hostServer'].values[0])
            StaticPage.portServerOut=int(df5['portServer'].values[0])
            StaticPage.nbTipo=df5['nbTipo'].values[0]
            sql ="SELECT * FROM powerbi_adm.conf_tipo WHERE nbTipo = %s;"
            StaticPage.cursor.execute(sql,(StaticPage.nbTipo,))
            resultado6 = StaticPage.cursor.fetchall()
            df6 = pd.DataFrame(resultado6)
            StaticPage.nmUsrOut=str(df6['nmUsr'].values[0])
            StaticPage.txPassOut=str(df6['txPass'].values[0])
            sql ="SELECT * FROM powerbi_adm.conf_server WHERE nbServer = %s;"
            StaticPage.cursor.execute(sql,(StaticPage.nbServerBi,))
            resultado7 = StaticPage.cursor.fetchall()
            df7 = pd.DataFrame(resultado7)
            StaticPage.hostServerIn=str(df7['hostServer'].values[0])
            StaticPage.portServerIn=int(df7['portServer'].values[0])
            StaticPage.nbTipoBi=df7['nbTipo'].values[0]
            sql = "SELECT * FROM powerbi_adm.conf_tipo WHERE nbTipo = %s"
            StaticPage.cursor.execute(sql,(StaticPage.nbTipoBi,))
            resultado8 = StaticPage.cursor.fetchall()
            df8 = pd.DataFrame(resultado8)
            StaticPage.nmUsrIn=str(df8['nmUsr'].values[0])
            StaticPage.txPassIn=str(df8['txPass'].values[0])
            sql = "SELECT * FROM powerbi_adm.conf_tipo WHERE nbTipo = %s"
            StaticPage.cursor.execute(sql,(3,))
            resultado9 = StaticPage.cursor.fetchall()
            df9 = pd.DataFrame(resultado9)
            StaticPage.nmUsrPowerbi=str(df9['nmUsr'].values[0])
            StaticPage.txPassPowerbi=str(df9['txPass'].values[0])
            StaticPage.conin = con.ConexionMariadb3(user=StaticPage.nmUsrIn,password=StaticPage.txPassIn,host=StaticPage.hostServerIn,port=StaticPage.portServerIn,database=StaticPage.dbBi)
            StaticPage.conin2 = con.ConexionMariadb2(user=StaticPage.nmUsrIn,password=StaticPage.txPassIn,host=StaticPage.hostServerIn,port=StaticPage.portServerIn,database=StaticPage.dbBi)
            StaticPage.conout = con.ConexionMariadb2(user=StaticPage.nmUsrOut,password=StaticPage.txPassOut,host=StaticPage.hostServerOut,port=StaticPage.portServerOut,database=StaticPage.dbSidis)
            StaticPage.conin3 = con.ConexionMariadb3(user=StaticPage.nmUsrIn,password=StaticPage.txPassIn,host=StaticPage.hostServerIn,port=StaticPage.portServerIn,database=StaticPage.dbBi)
            
    except mariadb.Error as e:
        print(logging.error(e))
