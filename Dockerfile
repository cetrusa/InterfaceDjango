FROM python:3.10
WORKDIR /code
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
VOLUME /code/staticfiles
VOLUME /code/media

# docker container run -d -p 4085:4084 
# -v static_volume:/code/staticfiles -v media_volume:/code/media cetrusa/interface-django:oso


CMD ["gunicorn", "--bind", "0.0.0.0:4084", "--timeout", "7200", "InterfaceDjango.wsgi:application"]