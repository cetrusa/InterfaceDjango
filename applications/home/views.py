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
from django.utils.decorators import method_decorator
from applications.users.decorators import registrar_auditoria
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from scripts.conexion import Conexion
from scripts.config import ConfigBasic
from scripts.StaticPage import StaticPage
from scripts.extrae_bi.extrae_bi import Extrae_Bi
from scripts.extrae_bi.cubo import Cubo_Ventas
from scripts.extrae_bi.interface import Interface_Contable
from django.contrib.auth.mixins import UserPassesTestMixin


from django.views.generic import (
    TemplateView
)
from applications.users.views import BaseView

class HomePage(LoginRequiredMixin, BaseView):
    template_name = "home/panel.html"
    login_url = reverse_lazy('users_app:user-login')
    
    @csrf_protect
    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        
        return redirect('home_app:panel')
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:panel'
        return context


class DownloadFileView(View):
    template_name=StaticPage.template_name
    login_url = reverse_lazy('users_app:user-login')
    def get(self, request):
        file_path = request.session.get('file_path')
        file_name = request.session.get('file_name')
        
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

class DeleteFileView(View):
    template_name=StaticPage.template_name
    login_url = reverse_lazy('users_app:user-login')
    def post(self, request):
        file_path = request.session.get('file_path')
        try:
            os.remove(file_path)
            # Cambia esto para redirigir al usuario
            return HttpResponseRedirect(reverse(self.template_name))
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})

    
class CuboPage(LoginRequiredMixin, BaseView):
    template_name = "home/cubo.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')

    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.cubo', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        database_name = request.POST.get('database_select')
        print(request.session.items())
        # database_name = request.session.get('database_name') or request.POST.get('database_select')
        print(database_name)
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')
        StaticPage.name = database_name
        try:
            cubo_ventas = Cubo_Ventas(database_name, IdtReporteIni, IdtReporteFin)
            cubo_ventas.Procedimiento_a_Excel()
            file_path = StaticPage.file_path
            file_name = StaticPage.archivo_cubo_ventas
            request.session['file_path'] = file_path
            request.session['file_name'] = file_name
            return JsonResponse({'success': True, 'error_message': '','file_path':file_path})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:cubo'
        return context
        
class InterfacePage(LoginRequiredMixin, BaseView):
    template_name = "home/interface.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')
    
    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.interface', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')
        StaticPage.name = database_name
        try:
            # Instanciamos la clase Interface_Contable con el nombre de la base de datos como argumento
            interface_contable = Interface_Contable(database_name, IdtReporteIni, IdtReporteFin)
            interface_contable.Procedimiento_a_Excel()
            file_path = StaticPage.file_path
            file_name = StaticPage.archivo_plano
            request.session['file_path'] = file_path
            request.session['file_name'] = file_name
            print(4)
            return JsonResponse({'success': True, 'error_message': '','file_path':file_path})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:interface'
        return context
        

class PlanoPage(LoginRequiredMixin, BaseView):
    template_name = "home/plano.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')

    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.plano', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        print(database_name)
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        IdtReporteIni = request.POST.get('IdtReporteIni')
        IdtReporteFin = request.POST.get('IdtReporteFin')
        StaticPage.name = database_name

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
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:plano'
        return context


class ActualizacionPage(LoginRequiredMixin, BaseView):
    template_name = "home/actualizacion.html"
    StaticPage.template_name = template_name
    login_url = reverse_lazy('users_app:user-login')

    @method_decorator(registrar_auditoria)
    @method_decorator(permission_required('permisos.actualizar_base', raise_exception=True))
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
            extrae_bi = Extrae_Bi(database_name)
            # Ejecutamos el script aquí
            extrae_bi.extractor()
            # extraebi = os.path.join('scripts','extrae_bi', 'extrae_bi.py')
            # subprocess.run(["python", extraebi])
            return JsonResponse({'success': True, 'error_message': ''})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error: no se pudo ejecutar el script. Razón: {e}"})
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:actualizacion'
        return context
    
class PruebaPage(LoginRequiredMixin, BaseView):
    template_name = "home/prueba.html"
    login_url = reverse_lazy('users_app:user-login')
    
    def post(self, request, *args, **kwargs):
        database_name = request.session.get('database_name') or request.POST.get('database_select')
        if not database_name:
            return redirect('home_app:panel')

        request.session['database_name'] = database_name
        StaticPage.name = database_name
        if not database_name:
            return JsonResponse({'success': False, 'error_message': 'Debe seleccionar una base de datos.'})
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = 'home_app:prueba'
        return context