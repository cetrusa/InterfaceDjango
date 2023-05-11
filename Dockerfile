# Pull base image
FROM python:3.10-alpine3.17
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code

RUN apk update \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev mysql-dev \
    && pip install --upgrade pip

# Install dependencies
COPY ./requirements.txt .

RUN pip install packaging
RUN pip install --no-cache-dir -r requirements.txt
# Copy project
COPY ./ ./
RUN python manage.py collectstatic --settings=InterfaceDjango.settings.prod --no-input 
CMD ["gunicorn", "--bind", "0.0.0.0:4085", "--timeout", "3600", "InterfaceDjango.wsgi:application"]
