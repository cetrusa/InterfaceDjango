from django.contrib import admin

# Register your models here.
from .models import ConfDt, ConfEmpresas, ConfServer, ConfSql, ConfTipo

admin.site.register(ConfDt)
admin.site.register(ConfEmpresas)
admin.site.register(ConfServer)
admin.site.register(ConfSql)
admin.site.register(ConfTipo)