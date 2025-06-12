API con DRF para Gestión de Clientes y Pedidos
Este proyecto es una API RESTful desarrollada con Django y Django REST Framework, diseñada para gestionar clientes y sus pedidos asociados. Incluye una base de datos de clientes profesional y una interfaz de documentación interactiva (Swagger UI) para facilitar la exploración y prueba de los endpoints.

🚀 Tecnologías Utilizadas
Python: Lenguaje de programación principal.

Django: Framework web de alto nivel para un desarrollo rápido y limpio.

Django REST Framework (DRF): Potente y flexible toolkit para construir APIs web.

django-cors-headers: Manejo de Cross-Origin Resource Sharing (CORS) para permitir solicitudes desde diferentes dominios.

drf-spectacular: Generación automática de documentación OpenAPI 3.0 (Swagger UI) para la API.

SQLite3: Base de datos predeterminada para desarrollo.

Git: Control de versiones.

Entornos Virtuales (venv): Para aislar las dependencias del proyecto.

✨ Características Principales
Gestión detallada de clientes con información profesional (nombre, apellido, email, dirección, etc.).

Gestión de pedidos asociados a cada cliente.

API RESTful para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en modelos Customer y Order.

Documentación interactiva de la API con Swagger UI, accesible a través de /api/schema/swagger-ui/.

⚙️ Configuración y Ejecución del Proyecto
Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

1. Clonar el Repositorio
Si aún no lo has hecho, clona este repositorio en tu máquina local:

git clone https://github.com/NicolasAndresCL/API_con_DRF.git
cd API_con_DRF

(Reemplaza tu-usuario y nombre-de-tu-repo con los datos de tu repositorio en GitHub.)

2. Crear y Activar el Entorno Virtual
Es fundamental usar un entorno virtual para gestionar las dependencias del proyecto de forma aislada.

python -m venv env

Activa el entorno virtual:

En Windows (CMD/PowerShell):

.\env\Scripts\activate

3. Instalar Dependencias
Con el entorno virtual activado, instala todas las librerías necesarias utilizando el archivo requirements.txt:

pip install -r requirements.txt

4. Realizar Migraciones de Base de Datos
Aplica las migraciones para crear las tablas de la base de datos (incluyendo los modelos Customer y Order):

python manage.py migrate

5. Crear un Superusuario
Necesitarás un superusuario para acceder al panel de administración de Django y gestionar los datos:

python manage.py createsuperuser

Sigue las indicaciones en la terminal para establecer el nombre de usuario, email y contraseña.

6. Ejecutar el Servidor de Desarrollo
Finalmente, inicia el servidor de desarrollo de Django:

python manage.py runserver

El servidor estará disponible en http://127.0.0.1:8000/.

📚 Documentación de la API (Swagger UI)
Una vez que el servidor esté en ejecución, puedes acceder a la documentación interactiva de la API (Swagger UI) en la siguiente URL:

http://127.0.0.1:8000/api/schema/swagger-ui/

Desde allí, podrás ver todos los endpoints disponibles (/api/customers/, /api/orders/, etc.), sus métodos (GET, POST, PUT, DELETE) y probar las solicitudes directamente desde el navegador.

Autenticación en Swagger UI:
Para probar los endpoints protegidos (ej. POST, PUT, DELETE), necesitarás autenticarte.

Haz clic en el botón "Authorize" (generalmente un candado verde en la esquina superior derecha).

En la sección tokenAuth (apiKey), en el campo Value, ingresa tu token de autenticación con el prefijo "Token " (por ejemplo: Token tu_token_largo_aqui).

Haz clic en "Authorize" para aplicar el token. Los candados junto a los endpoints deberían cerrarse.

🤝 Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor:

Haz un "fork" del repositorio.

Crea una nueva rama (git checkout -b feature/nueva-caracteristica).

Realiza tus cambios y haz commits descriptivos.

Abre un Pull Request.

¡Disfruta desarrollando con tu API de Django DRF!