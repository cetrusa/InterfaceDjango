from django.contrib import messages
import subprocess
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
import os
from django.http import HttpResponse,FileResponse,JsonResponse
import io
from django.views.generic import View
import requests


from scripts.conexion import Conexion
from scripts.config import ConfigBasic
from scripts.StaticPage import StaticPage
from scripts.extrae_bi.extrae_bi import Extrae_Bi
from scripts.extrae_bi.cubo import Cubo_Ventas
from scripts.extrae_bi.interface import Interface_Contable


from django.views.generic import (
    TemplateView
)

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/panel.html"
    login_url = reverse_lazy('users_app:user-login')
    
    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name


class DownloadFileView(View):
    template_name = "home/cubo.html"
    login_url = reverse_lazy('users_app:user-login')
    def get(self, request):
        file_path = request.session.get('file_path')
        file_name = request.session.get('file_name')
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

class DeleteFileView(View):
    template_name = "home/cubo.html"
    login_url = reverse_lazy('users_app:user-login')
    def post(self, request):
        file_path = request.session.get('file_path')
        try:
            os.remove(file_path)
            return JsonResponse({'success': True, 'error_message': ''
                                 })
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})

class CuboPage(LoginRequiredMixin, TemplateView):
    template_name = "home/cubo.html"
    login_url = reverse_lazy('users_app:user-login')

    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        print(f"cubo este es del post {database_name}")
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')

        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})
        try:
            # Instanciamos la clase Cubo_Ventas con el nombre de la base de datos como argumento
            cubo_ventas = Cubo_Ventas(database_name, IdtReporteIni, IdtReporteFin)
            cubo_ventas.Procedimiento_a_Excel()
            file_path = StaticPage.file_path
            print (file_path)
            file_name = StaticPage.archivo_cubo_ventas
            request.session['file_path'] = file_path
            request.session['file_name'] = file_name
            return JsonResponse({'success': True, 'error_message': '','file_path':file_path})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
class InterfacePage(LoginRequiredMixin, TemplateView):
    template_name = "home/interface.html"
    login_url = reverse_lazy('users_app:user-login')

    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        print(f"interface este es del post {database_name}")
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')
        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})
        try:
            # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
            interface_contable = Interface_Contable(database_name, IdtReporteIni, IdtReporteFin)
            interface_contable.Procedimiento_a_Excel()
            file_path = StaticPage.file_path
            file_name = StaticPage.archivo_cubo_ventas
            request.session['file_path'] = file_path
            request.session['file_name'] = file_name
            return JsonResponse({'success': True, 'error_message': '','file_path':file_path})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        

class PlanoPage(LoginRequiredMixin, TemplateView):
    template_name = "home/plano.html"
    login_url = reverse_lazy('users_app:user-login')

    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')
        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})
        try:
            # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
            interface_contable = Interface_Contable(database_name, IdtReporteIni, IdtReporteFin)
            interface_contable.Procedimiento_a_Plano()
            file_path = StaticPage.file_path
            file_name = StaticPage.archivo_plano
            request.session['file_path'] = file_path
            request.session['file_name'] = file_name
            return JsonResponse({'success': True, 'error_message': '','file_path':file_path})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})


class ActualizacionPage(LoginRequiredMixin, TemplateView):
    template_name = "home/actualizacion.html"
    login_url = reverse_lazy('users_app:user-login')

    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})
        try:
            # Instanciamos la clase Extrae_Bi con el nombre de la base de datos como argumento
            extrae_bi = Extrae_Bi(database_name)
            # Ejecutamos el script aquí
            extrae_bi.extractor()
            # extraebi = os.path.join('scripts','extrae_bi', 'extrae_bi.py')
            # subprocess.run(["python", extraebi])
            return JsonResponse({'success': True, 'error_message': ''})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
    
class PruebaPage(LoginRequiredMixin, TemplateView):
    template_name = "home/prueba.html"
    login_url = reverse_lazy('users_app:user-login')
    
    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})