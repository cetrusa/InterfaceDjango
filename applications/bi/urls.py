#
from django.urls import path

from . import views

app_name = "bi_app"

urlpatterns = [
    path(
        'actualizacion-bi/', 
        views.ActualizacionBiPage.as_view(),
        name='actualizacion_bi',
    ),
    path(
        'reporte-bi/', 
        views.EmbedReportPage.as_view(),
        name='reporte_bi',
    ),
    path('eliminar_reporte_fetched/', views.EliminarReporteFetched.as_view(), name='eliminar_reporte_fetched'),
    path('actualizar_database_name/', views.actualizar_database_name, name='actualizar_database_name'),
]