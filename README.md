# REST API: Gunicorn + Flask + MongoDB

# Instalación y configuración de ambiente

## pip + virtualenv

Instalación de dependencias utilizando pip

`pip install -r requirements.txt`

## Configuración: utilización de variables de entorno con dotenv

https://pypi.org/project/python-dotenv/

En el archivo `.env.dist` se encuentra una referencia de las variables de entorno requeridas

# Organización física y arquitectura

Se propone una arquitectura en capas en donde cada capa tiene un único objetivo y nível de abstracción.

Capas:

    * controller: administración de los requests
    * model: representación de modelo de datos 
    * schema: representación y validación de inputs/outputs de los requests
    * services -> servicios de administración de modelo de datos

```
src/ --> directorio principal
    /auth -> modulo de autorización
        /controllers -> ~ endpoints
        /models -> ~ modelos de datos
        /schemas -> ~ schemas input/output
        /services -> ~ servicios (abms)
        /test -> test cases
```

# Ejecución
## Run (dev)
export FLASK_APP=src/api/api.py flask run

## Run (gunicorn)
gunicorn --bind 0.0.0.0:5000 wsgi:app

## Run (docker)
`docker-compose build`
`docker-compose up -d app mongo`
