# 🧠 API RESTful en Django DRF: Gestión Modular de Clientes y Pedidos
Este proyecto es una API RESTful desarrollada con Django y Django REST Framework, orientada a la gestión de clientes y sus pedidos, bajo una arquitectura modular por dominio. La documentación interactiva está generada automáticamente mediante drf-spectacular, agrupada en Swagger UI por funcionalidades.

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
│   ├── auth_schema.py          # Vista decorada para token authentication (Swagger visible)
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

|Tecnología             	|Propósito                                                       |
|:-------------------------:|----------------------------------------------------------------|
|**Python**	                |Lenguaje principal del proyecto                                 |
|**Django**	                |Framework web robusto y escalable                               |
|**Django REST Framework**  |	Toolkit flexible para APIs                                   |
|**drf-spectacular**	    |Generación automática de documentación OpenAPI 3.0 + Swagger UI |
|**django-cors-headers**	|Configuración segura para CORS                                  |
|**SQLite3**	            |Base de datos default para entorno local                        |
|**Docker** (opcional)	    |Contenedorización para despliegue eficiente                     |
|**Git**	                |Control de versiones con flujo main/dev y commits convencionales|
|**venv**	                |Entornos virtuales para aislamiento limpio                      |

## ✨ Características Principales
🔹 CRUD completo en modelos Customer y Order, con relaciones entre ellos.

🔹 Modularización por dominio (customers, orders) mediante SimpleRouter y apps independientes.

🔹 Documentación extendida con @extend_schema, tags, summary, description por acción HTTP.

🔹 Endpoint de autenticación (POST /api/token/) separado en schema_auth.py con visibilidad asegurada en Swagger.

🔹 Ejemplos interactivos visibles en Swagger UI para endpoints protegidos.

🔹 Control de permisos por acción (AllowAny, IsAuthenticated, IsAdminUser) según lógica de negocio.

🔹 Integración de CORS para consumo externo desde frontend React u otros clientes.

## 📚 Documentación Interactiva (Swagger UI)
Una vez en ejecución, accede a:

'http://127.0.0.1:8000/api/schema/swagger-ui/'

Desde allí podrás:

Ver todos los endpoints disponibles agrupados por dominio (customers, orders)

Consultar detalles por método: GET, POST, PUT, DELETE

Autenticarse y probar endpoints protegidos vía JWT

## 🔐 Autenticación en Swagger UI:

Haz clic en "Authorize" (candado en la esquina superior derecha).

En tokenAuth, ingresa el token en formato:

Token tu_token_de_autenticación
Los candados se cerrarán para habilitar las operaciones protegidas.

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