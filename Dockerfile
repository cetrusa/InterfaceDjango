# Usamos la imagen oficial de Python 3.10 como imagen base
FROM python:3.10

# Crea un usuario y un grupo para ejecutar la aplicación
RUN groupadd -r interfacegroup && useradd -r -g interfacegroup adminuser
# Establecemos /code como el directorio de trabajo dentro del contenedor
WORKDIR /code

# Configuramos variables de entorno
# 1. Deshabilita la comprobación de la versión de pip
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# 2. Evita que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# 3. Asegura que las salidas de Python se impriman en tiempo real
ENV PYTHONUNBUFFERED 1

# Copiamos requirements.txt a /code en el contenedor
COPY ./requirements.txt .

# Instalamos las dependencias de Python especificadas en requirements.txt
# Usamos --no-cache-dir para prevenir que pip almacene los paquetes descargados
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todos los archivos y directorios al directorio de trabajo en el contenedor
COPY . .

# USER root
# ajustamos la zona horaria del contenedor
RUN ln -sf /usr/share/zoneinfo/America/Bogota /etc/localtime

# Cambia la propiedad del directorio /code/media al usuario y al grupo 'interfacesidis'
# RUN chown -R interfacesidis:interfacesidis /code/media
RUN chown -R root:root /code/media
# Cambiamos al usuario que acabamos de crear
# USER interfacesidis

# Ejecutamos el comando collectstatic de Django para recoger archivos estáticos
RUN python manage.py collectstatic --no-input

# Cambiar al usuario no root
USER adminuser

