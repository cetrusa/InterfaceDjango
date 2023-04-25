# Pull base image
FROM python:3.10
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY ./requirements.txt .
RUN pip install packaging && \
    pip install --no-cache-dir -r requirements.txt
# Copy project
COPY . .
RUN python manage.py collectstatic --no-input
CMD ["gunicorn", "--bind", "0.0.0.0:4084", "InterfaceDjango.wsgi:application"]