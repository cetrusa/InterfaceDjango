<p align="center">
  <a href="https://www.python.org/" target="_blank"><img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png" width="200" alt="Python Logo" /></a>
</p>


# Interface Django

1. Clonar proyecto
2. Ejecutar el modo dettached de docker-compose
```
docker compose up -d
```
### Correr la imagen en modo produccion

```
docker container run \
-d -p 4085:4084 \
-v static_volume:/code/staticfiles -v media_volume:/code/media \
cetrusa/interface-django:[VERSION]
```
