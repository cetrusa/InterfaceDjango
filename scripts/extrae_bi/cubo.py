from scripts.StaticPage import StaticPage
from scripts.conexion import Conexion
from scripts.config import ConfigBasic
import os
import pandas as pd
from sqlalchemy import create_engine, text
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
import logging

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    filemode="w",
)
logging.info("Inciando Proceso")


class Cubo_Ventas:
    def __init__(self, database_name, IdtReporteIni, IdtReporteFin):
        ConfigBasic(database_name)
        self.IdtReporteIni = IdtReporteIni
        self.IdtReporteFin = IdtReporteFin
        self.engine = create_engine("sqlite:///mydata.db")

    def connect_and_retrieve_data(self, sqlout, cursor, hoja):
        table_name = f"my_table_{StaticPage.name}_{hoja}"
        chunksize = 50000
        for chunk in pd.read_sql_query(sql=sqlout, con=cursor, chunksize=chunksize):
            chunk.to_sql(
                name=table_name, con=self.engine, if_exists="append", index=False
            )
        return table_name

    def write_to_excel(self, table_name, hoja, writer, chunksize=50000):
        for chunk in pd.read_sql_query(
            f"SELECT * FROM {table_name}", self.engine, chunksize=chunksize
        ):
            chunk.to_excel(writer, index=False, sheet_name=hoja, header=True)
            writer.sheets[hoja].sheet_state = "visible"

    def write_to_csv(self, table_name, chunksize=50000):
        StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{self.IdtReporteIni}_a_{self.IdtReporteFin}.csv"
        StaticPage.file_path = os.path.join("media", StaticPage.archivo_cubo_ventas)
        for chunk in pd.read_sql_query(
            f"SELECT * FROM {table_name}", self.engine, chunksize=chunksize
        ):
            chunk.to_csv(StaticPage.file_path, index=False, mode="a")

    def write_large_to_excel(self, table_name, hoja, chunksize=50000):
        StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{self.IdtReporteIni}_a_{self.IdtReporteFin}.xlsx"
        StaticPage.file_path = os.path.join("media", StaticPage.archivo_cubo_ventas)
        wb = Workbook(write_only=True)
        ws = wb.create_sheet(title=hoja)
        first_chunk = True
        for chunk in pd.read_sql_query(
            f"SELECT * FROM {table_name}", self.engine, chunksize=chunksize
        ):
            if first_chunk:
                ws.append(chunk.columns.tolist())
                first_chunk = False
            for index, row in chunk.iterrows():
                cells = [WriteOnlyCell(ws, value=value) for value in row]
                ws.append(cells)
        wb.save(StaticPage.file_path)

    def generate_sqlout(self, hoja):
        a = StaticPage.dbBi
        IdDs = ""
        compra = 0
        consig = 0
        nd = 0
        sql = StaticPage.nmProcedureExcel
        if StaticPage.dbBi == "powerbi_tym_eje":
            return text(
                f"CALL {sql}('{self.IdtReporteIni}','{self.IdtReporteFin}','{IdDs}','{hoja}','{compra}','{consig}','{nd}');"
            )
        else:
            return text(
                f"CALL {sql}('{self.IdtReporteIni}','{self.IdtReporteFin}','{IdDs}','{hoja}');"
            )

    def Procedimiento_a_Excel(self):
        if StaticPage.txProcedureExcel:
            for hoja in StaticPage.txProcedureExcel:
                # Generate the sqlout based on conditions
                sqlout = self.generate_sqlout(hoja)

                try:
                    with StaticPage.conin2.connect() as connectionout:
                        cursor = connectionout.execution_options(
                            isolation_level="READ COMMITTED"
                        )
                        table_name = self.connect_and_retrieve_data(
                            sqlout, cursor, hoja
                        )

                        with self.engine.connect() as connection:
                            total_records = connection.execute(
                                f"SELECT COUNT(*) FROM {table_name}"
                            ).fetchone()[0]

                        # Decide the format and write the data
                        if total_records > 1000000:
                            self.write_to_csv(table_name)
                        elif total_records > 250000:
                            self.write_large_to_excel(table_name, hoja)
                        else:
                            StaticPage.archivo_cubo_ventas = f"Cubo_de_Ventas_{StaticPage.name}_de_{self.IdtReporteIni}_a_{self.IdtReporteFin}.xlsx"
                            StaticPage.file_path = os.path.join(
                                "media", StaticPage.archivo_cubo_ventas
                            )
                            with pd.ExcelWriter(StaticPage.file_path) as writer:
                                self.write_to_excel(table_name, hoja, writer)
                    # Eliminar la tabla una vez que los datos se han escrito en Excel
                    with self.engine.connect() as connection:
                        connection.execute(f"DROP TABLE {table_name}")
                except Exception as e:
                    logging.info(f"No fue posible generar la información por {e}")

        else:
            return {
                "success": True,
                "error_message": f"La empresa {StaticPage.nmEmpresa} no maneja cubo",
            }
