import os,sys
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
from django.http import HttpResponse,FileResponse
from scripts.StaticPage import StaticPage
from scripts.conexion import Conexion
from scripts.config import ConfigBasic
import json
import msal
from django.core.exceptions import ImproperlyConfigured
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE

with open("secret.json") as f:
    secret = json.loads(f.read())

    def get_secret(secret_name, secrets=secret):
        try:
            return secrets[secret_name]
        except:
            msg = "la variable %s no existe" % secret_name
            raise ImproperlyConfigured(msg)

####################################################################
import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s", filemode="w")
####################################################################
logging.info('Inciando Proceso')

class Api_PowerBi:
    StaticPage = StaticPage()
    def __init__(self,database_name):
        ConfigBasic(database_name)

    def request_access_token_refresh(self):
        app_id = get_secret("CLIENT_ID")
        tenant_id = get_secret("TENANT_ID")

        authority_url = 'https://login.microsoftonline.com/' + tenant_id
        scopes = ['https://analysis.windows.net/powerbi/api/.default']

        # Step 1. Generate Power BI Access Token
        client = msal.PublicClientApplication(app_id, authority=authority_url)
        token_response = client.acquire_token_by_username_password(username=StaticPage.nmUsrPowerbi, password=StaticPage.txPassPowerbi, scopes=scopes)
        if not 'access_token' in token_response:
            raise Exception(token_response['error_description'])

        access_id = token_response.get('access_token')
        return access_id
    
    def run_datasetrefresh_solo_inicio(self):
        access_id = self.request_access_token_refresh()

        dataset_id = StaticPage.dataset_id_powerbi
        endpoint = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes'
        headers = {
            'Authorization': f'Bearer ' + access_id
        }

        response = requests.post(endpoint, headers=headers)
        if response.status_code == 202:
            print('Dataset refreshed')
        else:
            print(response.reason)
            print(response.json())

    def run_datasetrefresh(self):
        access_id = self.request_access_token_refresh()

        dataset_id = StaticPage.dataset_id_powerbi
        endpoint = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
        headers = {"Authorization": f"Bearer " + access_id}

        response = requests.post(endpoint, headers=headers)
        print(response)
        if response.status_code == 202:
            print("Dataset refreshed")
            self.get_status_history()
        elif response.status_code == 400:
            self.get_status_history()
        else:
            print(response.reason)
            print(response.json())
            
    def get_report_id(self):
        report_id= StaticPage.report_id_powerbi
        return report_id

    def generate_embed_token(self, report_id):
        access_id = self.request_access_token_refresh()

        # Reemplaza con el ID del grupo de trabajo en Power BI donde se encuentra el informe
        workspace_id = get_secret("GROUP_ID")

        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/GenerateToken'
        headers = {
            'Authorization': f'Bearer ' + access_id,
            'Content-Type': 'application/json'
        }
        payload = {
            "accessLevel": "View"
        }
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["token"]
        else:
            raise Exception("No se pudo generar el token de incrustación.")
        
    def get_status_history(self):
        access_id = self.request_access_token_refresh()

        dataset_id = StaticPage.dataset_id_powerbi
        endpoint = (
            f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes?$top=1"
        )
        headers = {"Authorization": f"Bearer " + access_id}

        max_attempts = 15  # Número máximo de intentos
        refresh_interval = 240  # Intervalo de espera en segundos
        attempt = 1

        while attempt <= max_attempts:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200 or response.status_code == 400:
                try:
                    refresh_status = response.json().get("value")[0].get("status")
                    if refresh_status in ["Completed", "Failed"]:
                        break
                    elif refresh_status == "Unknown":
                        print(
                            "The refresh is in progress. Attempt",
                            attempt,
                            "of",
                            max_attempts,
                        )
                except (json.decoder.JSONDecodeError, IndexError):
                    print("Failed to retrieve the refresh status.")
            else:
                print(response.reason)
                print(response.json())

            time.sleep(refresh_interval)
            attempt += 1

        if refresh_status == "Completed":
            print("The refresh completed successfully.")
        elif refresh_status == "Failed":
            error_message = response.json().get("value")[0].get("error")
            self.send_email(error_message)
            print("The refresh failed. Error message:", error_message)
        else:
            print(
                "The refresh did not complete within the specified number of attempts."
            )

    def send_email(self, error_message):
        host = "smtp.gmail.com"
        port = 587
        username = "torredecontrolamovil@gmail.com"
        password = "skmgumqcypkhykic"

        from_addr = "torredecontrolamovil@gmail.com"
        to_addr = ["cesar.trujillo@amovil.co", "soporte@amovil.co"]

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = COMMASPACE.join(to_addr)
        msg["Subject"] = f"Error Bi {StaticPage.nmEmpresa}"

        body = f"Error en el Bi de {StaticPage.nmEmpresa}, {error_message}"

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            server.quit()