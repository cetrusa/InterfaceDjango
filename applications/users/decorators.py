# from functools import wraps
# from applications.users.models import RegistroAuditoria
# import json
# from django.utils import timezone


# def grabar_auditoria(request, detalle):
#     # Obtenemos los datos de la petición
#     usuario = request.user
#     fecha_hora = timezone.now()
#     ip = request.META.get('REMOTE_ADDR')
#     transaccion = request.path_info
#     database_name = request.META.get('database_name')
#     city = request.META.get('CITY')

#     # Creamos una instancia del modelo RegistroAuditoria con los datos obtenidos
#     registro = RegistroAuditoria(usuario=usuario, fecha_hora=fecha_hora, ip=ip, transaccion=transaccion, detalle=detalle, database_name=database_name, city=city)
#     registro.save()

# def registrar_auditoria(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         # Ejecutamos la vista y obtenemos la respuesta
#         response = view_func(request, *args, **kwargs)
        
#         # Grabamos los datos de auditoría en la base de datos
#         detalle = {
#             'metodo': request.method,
#             'datos': request.POST.dict() if request.method == 'POST' else request.GET.dict()
#         }
#         grabar_auditoria(request, detalle)
        
#         return response
    
#     return wrapper
