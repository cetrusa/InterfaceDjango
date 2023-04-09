from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# from applications.users.decorators import registrar_auditoria
from django.urls import reverse_lazy, reverse
import requests
from django.http import HttpResponse,FileResponse,JsonResponse
from django.template.response import TemplateResponse
# Create your views here.
from django.views.generic import (
    TemplateView,View
)
from applications.users.views import BaseView
from scripts.embedded.powerbi import AadService,PbiEmbedService

from scripts.conexion import Conexion
from scripts.StaticPage import StaticPage
from scripts.extrae_bi.extrae_bi import Extrae_Bi
from scripts.extrae_bi.apipowerbi import Api_PowerBi
from scripts.config import ConfigBasic
from django.contrib.auth.decorators import login_required
from applications.users.decorators import registrar_auditoria
from scripts.embedded.powerbi import PbiEmbedService
from django.core.exceptions import ImproperlyConfigured
import json


with open("secret.json") as f:
    secret = json.loads(f.read())

    def get_secret(secret_name, secrets=secret):
        try:
            return secrets[secret_name]
        except:
            msg = "la variable %s no existe" % secret_name
            raise ImproperlyConfigured(msg)
        

class EliminarReporteFetched(View):
    def post(self, request, *args, **kwargs):
        if 'report_fetched' in request.session:
            del request.session['report_fetched']
            request.session.modified = True
        return JsonResponse({'success': True})
    
    
class ActualizacionBiPage(LoginRequiredMixin, BaseView):
    template_name = "bi/actualizacion.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')
    
    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.actualizacion_bi', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
                
    def post(self, request, *args, **kwargs):
        
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        StaticPage.name = database_name
        try:
            # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
            ApiPBi = Api_PowerBi(database_name)
            # Ejecutamos el script aquí
            ApiPBi.run_datasetrefresh()
            return JsonResponse({'success': True, 'error_message': ''})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'bi_app:actualizacion_bi'
        return context


def reporte_embed(request):
    # Utiliza la función get_embed_token_report() del módulo powerbi.py para obtener la información necesaria
    # para incrustar el informe de Power BI
    database_name = StaticPage.name
    ConfigBasic(database_name)
    clase = PbiEmbedService()
    embed_info_json = clase.get_embed_params_for_single_report(workspace_id=get_secret("GROUP_ID"), report_id=f"{StaticPage.report_id_powerbi}")
    embed_info = json.loads(embed_info_json)
    
    # Imprime la información de embed_info para depurar
    print("embed_info:", embed_info)
    # Verifica si se ha producido algún error al obtener la información de incrustación
    if 'error' in embed_info:
        context = {'error_message': embed_info['error']}
    else:
        context = {
            'EMBED_URL': embed_info['reportConfig'][0]['embedUrl'],
            'EMBED_ACCESS_TOKEN': embed_info['accessToken'],
            'REPORT_ID': embed_info['reportConfig'][0]['reportId'],
            'TOKEN_TYPE': 1,  # Establece en 1 para utilizar el token de incrustación
            'TOKEN_EXPIRY': embed_info['tokenExpiry'],  # Agrega tokenExpiry al contexto
            'form_url': 'bi_app:reporte_embed2'  # Agrega form_url al contexto
            }

    return render(request, 'bi/reporte_embedv2.html', context)

class IncrustarBiPage(LoginRequiredMixin, BaseView):
    template_name = "bi/reporte_embed.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')

    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.informe_bi', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def process_request(self, request):
        print(request.session.items())
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        print(database_name)
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        StaticPage.name = database_name
        try:
            ConfigBasic(database_name)
            clase = PbiEmbedService()
            embed_info_json = clase.get_embed_params_for_single_report(workspace_id=get_secret("GROUP_ID"), report_id=f"{StaticPage.report_id_powerbi}")
            embed_info = json.loads(embed_info_json)
            if 'error' in embed_info:
                context = {'error_message': embed_info['error']}
            else:
                context = {
                    'EMBED_URL': embed_info['reportConfig'][0]['embedUrl'],
                    'EMBED_ACCESS_TOKEN': embed_info['accessToken'],
                    'REPORT_ID': embed_info['reportConfig'][0]['reportId'],
                    'TOKEN_TYPE': 1,  # Establece en 1 para utilizar el token de incrustación
                    'TOKEN_EXPIRY': embed_info['tokenExpiry'],  # Agrega tokenExpiry al contexto
                    'form_url': 'bi_app:reporte_embed'  # Agrega form_url al contexto
                }

            return context
        except Exception as e:
            return {'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"}

    def post(self, request, *args, **kwargs):
        context = self.process_request(request)
        if 'error_message' in context:
            context = {'error_message': context.get('error')}
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.process_request(request)
        if 'error_message' in context:
            context = {'error_message': context.get('error')}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context





        
# esta clase es para embebido normalito de la url publica
# class EmbedReportPage(LoginRequiredMixin, BaseView):
#     template_name = "bi/reporte_bi.html"
#     StaticPage.template_name = template_name
#     login_url = reverse_lazy('users_app:user-login')
    
#     @method_decorator(registrar_auditoria)
#     @method_decorator(permission_required('permisos.informe_bi', raise_exception=True))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         database_name = request.POST.get('database_select')
        
#         if not database_name:
#             return redirect('home_app:panel')
        
#         request.session['database_name'] = database_name
#         try:
#             config = ConfigBasic(database_name)    
#             url_powerbi= config.StaticPage.url_powerbi
#             return JsonResponse({'url_powerbi': url_powerbi})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_url'] = 'bi_app:reporte_bi'
#         return context