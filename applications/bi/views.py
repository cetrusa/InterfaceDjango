from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# from applications.users.decorators import registrar_auditoria
from django.urls import reverse_lazy, reverse
import requests
from django.http import HttpResponse,FileResponse,JsonResponse
# Create your views here.
from django.views.generic import (
    TemplateView,View
)

from scripts.conexion import Conexion
from scripts.StaticPage import StaticPage
from scripts.extrae_bi.extrae_bi import Extrae_Bi
from scripts.extrae_bi.apipowerbi import Api_PowerBi
from scripts.config import ConfigBasic
from django.contrib.auth.decorators import login_required
from applications.users.decorators import registrar_auditoria

@login_required(login_url='/login/')
def actualizar_database_name(request):
    database_name = request.POST.get('database_select')
    request.session['database_name'] = database_name
    return JsonResponse({'success': True})

class EliminarReporteFetched(View):
    def post(self, request, *args, **kwargs):
        if 'report_fetched' in request.session:
            del request.session['report_fetched']
            request.session.modified = True
        return JsonResponse({'success': True})
    
    
class ActualizacionBiPage(LoginRequiredMixin, TemplateView):
    template_name = "bi/actualizacion.html"
    login_url = reverse_lazy('users_app:user-login')
    
    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.actualizacion_bi', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.get_all_permissions())  # Imprime los permisos del usuario
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('users_app:user-login')
            
    def post(self, request, *args, **kwargs):
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        try:
            # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
            ApiPBi = Api_PowerBi(database_name)
            # Ejecutamos el script aquí
            ApiPBi.run_datasetrefresh()
            return JsonResponse({'success': True, 'error_message': ''})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
    
class EmbedReportPage(LoginRequiredMixin, TemplateView):
    template_name = "bi/reporte_bi.html"
    login_url = reverse_lazy('users_app:user-login')
    
    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.informe_bi', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.get_all_permissions())  # Imprime los permisos del usuario
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('users_app:user-login')

    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        request.session['database_name'] = database_name
        if not database_name:
            return redirect('home_app:panel')
        
        print(f"embebed este es del post {database_name}")

        try:
            config = ConfigBasic(database_name)    
            url_powerbi= config.StaticPage.url_powerbi
            print(url_powerbi)
            return JsonResponse({'url_powerbi': url_powerbi})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        

