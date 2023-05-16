# Usamos la imagen oficial de Python 3.10 como imagen base
FROM python:3.10

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

# Ejecutamos el comando collectstatic de Django para recoger archivos estáticos
RUN python manage.py collectstatic --no-input

# Definimos los volúmenes para los datos que deben persistir entre ejecuciones del contenedor
VOLUME /code/staticfiles
VOLUME /code/media

# Especificamos el comando que se ejecutará cuando se inicie el contenedor
# Iniciamos un servidor Gunicorn que sirve la aplicación Django
CMD ["gunicorn", "--bind", "0.0.0.0:4085", "--timeout", "84000", "InterfaceDjango.wsgi:application"]
