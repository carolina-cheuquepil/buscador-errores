# Buscador de Errores Dimarsa

Aplicacion web hecha con Django y Bootstrap 5 para buscar, administrar y mantener un catalogo de errores, soluciones, responsables, departamentos y pruebas.

## Funciones principales

- Busqueda por texto libre en descripcion, causa, soluciones, anexos, comentarios, usuario y modulo.
- Filtros por hardware, sistema y frecuencia.
- Lista paginada de errores con detalle completo.
- CRUD de errores, soluciones, responsables, departamentos, hardware, sistemas y pruebas.
- Catalogo de soluciones reutilizables, con asignacion de responsables y departamentos.
- Modal rapido para crear o editar soluciones desde el formulario de errores.
- Asignacion de encargados mediante casillas, para poder marcar y desmarcar responsables sin usar combinaciones de teclado.
- Contactos por departamento.
- Login obligatorio para usar la aplicacion.
- Bloqueo temporal despues de varios intentos fallidos de login.
- Panel de administracion de Django en `/admin/`.
- Importador desde Excel con `python manage.py importar_excel`.

## Requisitos

- Python 3.10 o superior.
- MySQL si se usara una base remota o compartida.
- SQLite no requiere servidor adicional y queda como configuracion local por defecto.

## Instalacion local

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

En macOS o Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno si usaras MySQL:

```powershell
$env:DJANGO_SECRET_KEY="cambia-esta-clave"
$env:DJANGO_DEBUG="True"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
$env:DB_ENGINE="django.db.backends.mysql"
$env:DB_NAME="errores_dimarsa"
$env:DB_USER="usuario"
$env:DB_PASSWORD="password"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
```

Si no configuras `DB_ENGINE`, Django usara SQLite en `db.sqlite3`.

4. Crear o actualizar la base de datos:

```bash
python manage.py migrate
```

5. Importar datos desde Excel:

```bash
python manage.py importar_excel "ruta/al/errores Dimarsa.xlsx"
```

Para borrar datos previos antes de importar:

```bash
python manage.py importar_excel "ruta/al/errores Dimarsa.xlsx" --reset
```

6. Crear un usuario administrador, opcional:

```bash
python manage.py createsuperuser
```

Tambien puedes crear usuarios desde `/admin/` una vez que entres con el superusuario.

7. Levantar el servidor:

```bash
python manage.py runserver
```

Abrir:

- Buscador: <http://127.0.0.1:8000/>
- Login: <http://127.0.0.1:8000/login/>
- Admin: <http://127.0.0.1:8000/admin/>

## Rutas principales

- `/`: listado y busqueda de errores.
- `/login/`: inicio de sesion.
- `/logout/`: cierre de sesion por POST.
- `/error/nuevo/`: crear error.
- `/soluciones/`: administrar soluciones.
- `/responsables/`: administrar responsables.
- `/departamentos/`: administrar departamentos y contactos.
- `/plataforma/hardware/`: administrar hardware.
- `/plataforma/sistemas/`: administrar sistemas y modulos.
- `/pruebas/`: administrar pruebas.

## Estructura

```text
buscador_errores/
|-- manage.py
|-- requirements.txt
|-- README.md
|-- buscador_errores/          # Configuracion del proyecto Django
|-- errores/                   # App principal
|   |-- dominios/              # Modelos separados por dominio
|   |-- management/commands/   # Comando importar_excel
|   |-- forms.py
|   |-- views.py
|   |-- urls.py
|-- templates/errores/         # Plantillas HTML
|-- static/                    # Archivos estaticos locales
```

## Archivos que no se suben a GitHub

El `.gitignore` excluye entorno virtual, cache de Python, bases SQLite, archivos `.env`, medios subidos, backups y archivos Excel/JSON con datos locales. Si necesitas compartir datos de ejemplo, crea un archivo anonimizado.

## Notas de seguridad

- No subas claves, passwords, bases de datos reales ni Excel con informacion interna.
- Configura credenciales mediante variables de entorno en el servidor.
- Para produccion, usa `DJANGO_DEBUG=False` y define `DJANGO_ALLOWED_HOSTS` con los dominios permitidos.
- Define `DJANGO_SECRET_KEY` con una clave unica y privada.
- Publica el sitio solo con HTTPS. Si el proxy o hosting ya entrega HTTPS, configura las variables `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `CSRF_TRUSTED_ORIGINS` y `USE_X_FORWARDED_PROTO` segun el entorno.
- El login usa usuarios de Django, validadores de contrasena y bloqueo temporal por intentos fallidos.
- El logout se hace por POST con CSRF.
