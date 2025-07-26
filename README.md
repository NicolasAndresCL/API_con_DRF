# 🧠 API RESTful en Django DRF: Gestión Modular de Clientes, Productos y Pedidos
Este proyecto es una API RESTful desarrollada con Django y Django REST Framework, orientada a la gestión de clientes, productos y sus pedidos, bajo una arquitectura modular por dominio. La documentación interactiva está generada automáticamente mediante drf-spectacular, agrupada en Swagger UI por funcionalidades.

```
API_con_DRF/
├── customers/                  # App para gestión de clientes
│   ├── migrations/             # Migraciones del modelo Customer
│   ├── __init__.py
│   ├── models.py               # Modelo Customer
│   ├── serializers.py          # Serializador de clientes
│   ├── views.py                # CustomerViewSet con permisos y validación
│   ├── urls.py                 # Rutas /api/customers/
│   ├── apps.py                 # Registro de esquema personalizado
│   ├── schema_auth.py          # Vista decorada para token authentication (Swagger visible)
│   └── tests.py
│
├── orders/                    # App para gestión de pedidos
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py               # Modelo Order
│   ├── serializers.py
│   ├── signals.py
│   ├── views.py                # OrderViewSet con documentación extendida
│   ├── urls.py
│   └── tests.py
│
├── products/                  # App para gestión de productos
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py               # Modelo Product
│   ├── serializers.py
│   ├── views.py                # ProductViewSet con lógica de stock y acciones personalizadas
│   ├── urls.py
│   └── tests.py
│
├── django_crud_api/           # Proyecto principal
│   ├── __init__.py
│   ├── settings.py             # Configuración global: DRF, CORS, Swagger
│   ├── urls.py                 # Rutas centrales: Swagger, /api/token/, modularización por apps
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3                 # Base de datos local (desarrollo)
├── manage.py                  # Script principal para comandos Django
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación técnica y guía de instalación

```
## 🚀 Tecnologías Utilizadas

|Tecnología             	 |Propósito                                                       |
|:--------------------------:|----------------------------------------------------------------|
|**Python**	                 |Lenguaje principal del proyecto                                 |
|**Django**	                 |Framework web robusto y escalable                               |
|**Django REST Framework**   |	Toolkit flexible para APIs                                    |
|**drf-spectacular**	     |Generación automática de documentación OpenAPI 3.0 + Swagger UI |
|**django-cors-headers**	 |Configuración segura para CORS                                  |
|**rest_framework_simplejwt**|Autenticación segura basada en tokens JWT                       |
|**django-environ**          |Configuración sensible vía .env                                 |
|**MySQL**	                 |Soporte para entornos de desarrollo y producción                |
|**Git**	                 |Control de versiones con flujo main/dev y commits convencionales|
|**venv**	                 |Entornos virtuales para aislamiento limpio                      |

## ✨ Características Principales

🔹 Autenticación JWT integrada vía djangorestframework-simplejwt, documentada en Swagger con ejemplos interactivos.

🔹 Modularización por dominio: cada app (customers, products, orders) define sus modelos, vistas, rutas y esquema.

🔹 Swagger agrupado por tags: "Customers", "Orders", "Products", "Authentication" — cada endpoint documentado por acción.

🔹 Documentación extendida con @extend_schema, tags, summary, description por acción HTTP.

🔹 Endpoint de autenticación (POST /api/token/) separado en schema_auth.py con visibilidad asegurada en Swagger.

🔹 Ejemplos interactivos visibles en Swagger UI para endpoints protegidos.

🔹 Control de permisos por acción (AllowAny, IsAuthenticated, IsAdminUser) según lógica de negocio.

🔹 Integración de CORS para consumo externo desde frontend React u otros clientes.

⚙️ Configuración segura en settings.py usando django-environ y .env excluido del repo por .gitignore.

🧪 Esquema exportable (schema.yml) generado por drf-spectacular, válido para integraciones externas.

## 📚 Documentación Interactiva (Swagger UI)
Una vez en ejecución, accede a:

'http://127.0.0.1:8000/api/schema/swagger-ui/'

Desde allí podrás:

Ver todos los endpoints disponibles agrupados por dominio (customers, orders)

Consultar detalles por método: GET, POST, PUT, DELETE

Autenticarse y probar endpoints protegidos vía JWT

## 🔐 Formato correcto para el token:

En jwtAuth, ingresá:
```
Bearer <access_token>
Ejemplo:

Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```
## ⚙️ Ejecución Local

- Clonar el repositorio

```git clone https://github.com/NicolasAndresCL/API_con_DRF.git
cd API_con_DRF
```

- Crear entorno virtual
```
python -m venv env
source env/bin/activate  # En Linux/Mac
.\env\Scripts\activate    # En Windows/CMDER
```
- Instalar dependencias
```
pip install -r requirements.txt
```
- Aplicar migraciones
```
python manage.py migrate
```
- Crear superusuario
```
python manage.py createsuperuser
```
- Ejecutar servidor
```
python manage.py runserver
```
## 🧪 Testing y Buenas Prácticas

✅ Versionado completo en rama dev con commits descriptivos estilo convencional.

✅ Código modularizado por dominio, siguiendo principios de desacoplamiento lógico.

✅ Documentación Swagger autoactualizada al crear o modificar endpoints.

✅ Separación clara entre lógica de negocio, serialización y esquema/documentación.

✅ Uso de drf-spectacular para control absoluto del OpenAPI Schema.

### 🔄 Configuración segura de Celery + Redis

Variables definidas en `.env`:
- `CELERY_BROKER_URL`: URL del broker (Redis en este caso)
- `CELERY_RESULT_BACKEND`: Almacén de resultados (también Redis)
- `CELERY_ACCEPT_CONTENT`: Formato aceptado (`json`)
- `CELERY_TASK_SERIALIZER`: Serializador de tareas (`json`)

Configuración cargada en `settings.py` vía `django-environ`, asegurando flexibilidad y seguridad 🔐


## 🤝 Contribuciones
 Las mejoras técnicas y visuales son bienvenidas. Para contribuir:

bash
```
# Crear rama nueva
git checkout -b feature/nueva-caracteristica

# Commit limpio y descriptivo
git commit -m "feat: agregar validación de email en modelo Customer"

# Push y Pull Request
```
## 🌐 Portafolio Técnico
Accede a la documentación completa en Swagger UI, ejemplos interactivos y despliegue dockerizado desde:

🔗 https://nicolasandrescl.pythonanywhere.com

Incluye:

Swagger UI completo por dominio

Documentación con ejemplos interactivos

Validación en tiempo real de flujos autenticados

API limpia y profesional para entrevistas técnicas o uso externo
## 📄 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
## 📝 Notas Finales
Este proyecto es un ejemplo de buenas prácticas en Django REST Framework, con un enfoque modular y una documentación interactiva que facilita su uso y comprensión. Ideal para desarrolladores que buscan una base sólida para construir APIs RESTful escalables y mantenibles.