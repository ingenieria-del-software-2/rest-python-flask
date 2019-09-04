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
        /controllers -> endpoints
        /models -> modelos de datos
        /schemas -> schemas input/output
        /services -> servicios (adm modelo de datos)
```

# Almacenamiento de password
En lugar de almacenar la contraseña en texto plano se almacenará un hash de la misma utilizando la biblioteca `haslib`.

https://docs.python.org/3/library/hashlib.html

# Autorización
Para verificar e identificar a un usuario se utilizará un mecanismo básado en la generación de un token cifrado con la información del usuario.
 
Para implementar este mecanismo se utiliza JWT. 

https://pyjwt.readthedocs.io/en/latest/

decorators: https://realpython.com/primer-on-python-decorators/

https://eddmann.com/posts/using-basic-auth-and-decorators-in-pythons-flask/

## Login
```
curl -XPOST http://localhost:5000/api/v1/auth/login -d '{"username":"gfusca", "password":"123456"}' -H "Content-Type: application/json"

POST /api/v1/auth/login HTTP/1.1
> Host: localhost:5000
> Content-Type: application/json
< HTTP/1.1 200 OK
< Content-Type: application/json
{   
    "email":"gfuscax@gmail.com",
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImdmdXNjYSIsImVtYWlsIjoiZ2Z1c2NheEBnbWFpbC5jb20if",
    "username":"gfusca"
}
```

## Utilización de token
```
curl -v -XGET http://localhost:5000/api/v1/secret/secure -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImdmdXNjYSIsImVtYWlsIjoiZ2Z1c2NheEBnbWFpbC5jb20ifQ.XTt7jRuTZ_gV9FSMffbFsdRuNwT44CR0TIAYwQpa7ZA"
> GET /api/v1/secret/secure HTTP/1.1
> Host: localhost:5000
> Content-Type: application/json
> Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImdmdXNjYSIsImVtYWlsIjoiZ2Z1c2NheEBnbWFpbC5jb20ifQ.XTt7jRuTZ_gV9FSMffbFsdRuNwT44CR0TIAYwQpa7ZA
>
< HTTP/1.1 200 OK
< Content-Type: application/json
{
    "data": "Secure!"
}
```

# Ejecución

## Run (dev)
export FLASK_APP=src/api/api.py flask run

## Run (gunicorn)
gunicorn --bind 0.0.0.0:5000 wsgi:app

## Run (docker)
`docker-compose build`
`docker-compose up -d app mongo`

# Test + Coverage
Para la ejecución de test unitarios y la generacion de reporte de coverage se utiliza `pytest`

*Ejemplo de ejecución*

`python -m pytest --cov --cov-report html`

