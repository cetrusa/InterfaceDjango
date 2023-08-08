import win32com.client
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE
from email import encoders
import smtplib
import datetime
import markdown

# Declara las variables globales
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

file_path = "G:\\OneDrive\\OneDrive - Asistencia Movil SAS\\Compi (Bi).xlsx"

# Ruta al archivo en la carpeta de OneDrive sincronizada
# file_path = 'https://asistenciamovil-my.sharepoint.com/:x:/g/personal/cesar_trujillo_amovil_co/Eb_ManrwD1NDpLQeXTvVmlkB_JNalRCqbit37wapAY0kig?e=LQ0Z07'

local_copy_path = (
    "G:\\OneDrive\\OneDrive - Asistencia Movil SAS\\compi_bi_{}.xlsx".format(timestamp)
)

macro_name = "UpdateSlicer"  # Nombre de la macro que creaste en VBA


def list_slicer_names():
    global file_path
    # Open Excel and the file you want to update
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    workbook = excel.Workbooks.Open(file_path)

    # Try to access SlicerCaches in the workbook
    try:
        slicer_caches = workbook.SlicerCaches
        for slicer_cache in slicer_caches:
            # Print the name of each SlicerCache
            print(f"Slicer Cache Name: {slicer_cache.Name}")
    except Exception as e:
        # Ignore if unable to access SlicerCaches
        print(f"Error accessing SlicerCaches: {e}")

    # Close the file without saving and quit Excel
    workbook.Close(SaveChanges=False)
    excel.Quit()


def Refresh_Excel():
    # Indica que vas a usar las variables globales
    global file_path, local_copy_path, macro_name

    # Abre Excel y el archivo que deseas actualizar
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    workbook = excel.Workbooks.Open(file_path)

    # Obtiene la fecha actual
    current_date = datetime.datetime.now()
    current_month_name = current_date.strftime("%Y%m")
    # Obtiene la fecha un mes atrás
    last_month_date = current_date - datetime.timedelta(
        days=10
    )  # puedes ajustar los días si es necesario
    last_month_name = last_month_date.strftime("%Y%m")

    # Verifica si el valor actual del slicer es el mismo que el mes actual
    slicer_cache = workbook.SlicerCaches("SegmentaciónDeDatos_Período")
    print(slicer_cache.VisibleSlicerItemsList)

    current_month_value = "[Calendario].[Período].&[" + current_month_name + "]"

    if slicer_cache.VisibleSlicerItemsList == [current_month_value]:
        print("El slicer ya está seleccionado en el mismo valor.")
        # Actualiza las conexiones sin ejecutar la macro completa
        for connection in workbook.Connections:
            connection.Refresh()
    else:
        print("Seleccionando nuevo valor en el slicer...")
        # Limpia los filtros del slicer
        # slicer_cache.ClearAllFilters()
        # Establece el valor deseado en la lista de elementos visibles
        slicer_cache.VisibleSlicerItemsList = [current_month_value]
        # Actualiza las conexiones sin ejecutar la macro completa
        for connection in workbook.Connections:
            connection.Refresh()

    time.sleep(10)
    # workbook.Save()

    # Espera un poco para asegurarse de que OneDrive sincronice los cambios
    time.sleep(2)  # Espera 2 segundos, puedes ajustar este valor

    # Guarda una copia del archivo
    workbook.SaveCopyAs(local_copy_path)
    workbook.Close(SaveChanges=False)
    # Abre la copia local
    copy_workbook = excel.Workbooks.Open(local_copy_path)

    # Elimina conexiones
    for connection in copy_workbook.Connections:
        connection.Delete()
        
    time.sleep(2)  # Espera 2 segundos, puedes ajustar este valor

    # copy_workbook.SlicerCaches("SegmentaciónDeDatos_Período").Delete()

    # Guarda y cierra la copia local
    copy_workbook.Save()
    copy_workbook.Close()

    # Cierra Excel
    excel.Quit()

    # Espera un poco para asegurarse de que OneDrive sincronice los cambios
    time.sleep(2)  # Espera 2 segundos, puedes ajustar este valor
    
    send_email()
    


def send_email():
    # Indica que vas a usar las variables globales
    global local_copy_path

    host = "smtp.gmail.com"
    port = 587
    username = "torredecontrolamovil@gmail.com"
    password = "skmgumqcypkhykic"

    from_addr = "torredecontrolamovil@gmail.com"
    to_addr = [
        "cesar.trujillo@amovil.co",
    ]
    with open("difusion.txt", "r") as file:
        cc_addr = [line.strip() for line in file]

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = COMMASPACE.join(to_addr)
    msg["Cc"] = COMMASPACE.join(cc_addr)
    msg["Subject"] = "Analitica Compi tienda"

    # logo_path = "logouau.png"

    # with open(logo_path, "rb") as logo_file:
    #     logo_data = logo_file.read()

    # logo_image = MIMEImage(logo_data)
    # logo_image.add_header("Content-ID", "<logo>")
    # msg.attach(logo_image)
    
    html_message = f"""
    <html>
        <head>
        <style>
        body {{ font-family: Arial; }}
        p {{ font-size: 12px; }}
        </style>
        </head>
        <body>
            <h3>Cordial Saludo,</h3>
            <p>Adjunto encontrará el seguimiento acumulado de Compi tienda, cuya información corresponde al mes actual y hace referencia a las cifras consolidadas en la aplicación.</p>
            <p>Mensaje generado de manera automática, por favor no responder.</p>
            <br>
            <img src="https://drive.google.com/uc?export=view&id=1nCnHpLIepkZ37MJPuAxcOMyeq0Bg2Iny" alt="Logo de la empresa">
        </body>
    </html>
    """

    msg.attach(MIMEText(html_message, "html"))

    filename = local_copy_path.split("\\")[-1]
    local_copy_path
    with open(local_copy_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    msg.attach(part)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, to_addr + cc_addr, msg.as_string())
        server.quit()

    # Elimina el archivo una vez enviado
    try:
        os.remove(local_copy_path)
        print("Archivo eliminado exitosamente.")
    except Exception as e:
        print(f"Error al eliminar el archivo: {e}")
