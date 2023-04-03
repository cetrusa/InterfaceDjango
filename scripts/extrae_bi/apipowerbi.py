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
    
    def run_datasetrefresh(self):
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