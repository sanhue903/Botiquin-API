# backend de la app web "El Botiquin de las Emociones"
version de Python 3.9

para instalar las dependencias recuerda utilizar un entorno virtual con el siguiente comando:
`python (o python3) -m venv .venv`

para entrar al entorno virtual utiliza lo siguiente si es en windows git bash:
`source .venv/Scripts/activate`

si es linux:
`source .venv/bin/activate`

luego instala las dependencias:
`pip install -r requirements.txt`

por ultimo utiliza postman para registrar un usuario admin:
- `http://127.0.0.1:5000/auth/signup`
obten el token del admin:
- `http://127.0.0.1:5000/auth/login`
y por ultimo registra la aplicacion del archivo botiquin.json utilizando el token:
- `http://127.0.0.1:5000/apps/register`
