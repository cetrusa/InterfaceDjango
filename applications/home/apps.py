from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.home'

    # def ready(self):
    #         # Importamos el módulo de permisos
    #         from django.contrib.auth.models import Permission
    #         from django.contrib.contenttypes.models import ContentType

    #         # Creamos un ContentType ficticio para nuestros permisos personalizados
    #         content_type, _ = ContentType.objects.get_or_create(
    #             app_label=self.name,
    #             model='home_permisos'
    #         )

    #         # Definimos permisos personalizados
    #         permissions = [
    #             ('nav_bar', 'Ver la barra de menú'),
    #             ('cubo', 'Generar cubo de ventas'),
    #             ('interface', 'Generar interface contable'),
    #             ('plano', 'Generar archivo plano'),
    #             ('informe_bi', 'Informe Bi'),
    #             ('actualizar_base', 'Actualzación de datos'),
    #             ('actualizacion_bi', 'Actualizar Bi'),
    #             ('nuevo', 'nueva opción'),
    #         ]

    #         # Añadimos los permisos personalizados al ContentType ficticio
    #         for codename, name in permissions:
    #             Permission.objects.get_or_create(
    #                 codename=codename,
    #                 name=name,
    #                 content_type=content_type
    #             )