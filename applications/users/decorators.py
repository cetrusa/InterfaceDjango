from functools import wraps
from applications.users.models import RegistroAuditoria
import json
from django.utils import timezone
import geocoder
from scripts.StaticPage import StaticPage

def grabar_auditoria(request, detalle):
    # Obtenemos los datos de la petición
    gc = geocoder.ip("me")
    usuario = request.user
    ip = gc.ip
    transaccion = request.path_info
    database_name = StaticPage.name
    city = gc.city

    # Creamos una instancia del modelo RegistroAuditoria con los datos obtenidos
    registro = RegistroAuditoria(usuario=usuario, ip=ip, transaccion=transaccion, detalle=detalle, database_name=database_name, city=city)
    registro.save()

def registrar_auditoria(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Ejecutamos la vista y obtenemos la respuesta
        response = view_func(request, *args, **kwargs)
        
        # Grabamos los datos de auditoría en la base de datos
        detalle = {
            'metodo': request.method,
            'datos': request.POST.dict() if request.method == 'POST' else request.GET.dict()
        }
        grabar_auditoria(request, detalle)
        
        return response
    
    return wrapper
