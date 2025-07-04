"""
Django settings for django_crud_api project.

Generated by 'django-admin startproject' using Django 5.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_troawpv-sm6h7*!eqn#lkh2s55%mb0$yqbv&cx5+^esnu4bzb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # Middleware para manejar CORS
    'customers',  # Aplicación personalizada para manejar clientes
    'products',  # Aplicación personalizada para manejar productos
    'orders', # Aplicación personalizada para manejar pedidos
    'rest_framework', # Django REST Framework
    'rest_framework.authtoken',  # Para autenticación basada en tokens
    'drf_spectacular', # Para generar documentación OpenAPI
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Middleware para manejar CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_crud_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_crud_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'api_drf_db',
        'USER': 'root',
        'PASSWORD': 'Kerubin7$',
        'HOST': 'localhost',  # o la IP si es remoto
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# cors authorization
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication', # Recomendado para APIs RESTful
        # 'rest_framework.authentication.BasicAuthentication', # Opcional, para testing rápido
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Requiere autenticación por defecto para todas las rutas
        # O podrías usar:
        # 'rest_framework.permissions.AllowAny', # Permite acceso sin autenticación (menos seguro por defecto)
        # 'rest_framework.permissions.IsAdminUser', # Solo admins
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Gestión de Clientes, Pedidos y Productos',
    'DESCRIPTION': 'Documentación de la API RESTful para la gestión integral de clientes, la administración de pedidos y el catálogo de productos.', # <--- Opcional: una descripción
    'VERSION': '1.0.0', # <--- Opcional: la versión de tu API
    'SERVE_INCLUDE_SCHEMA': False, # Opcional: para no incluir el esquema OpenAPI directamente en la página
    # Otras configuraciones si las necesitas, por ejemplo para autenticación:
    'SECURITY': [
        {
            'TokenAuth': {
                'type': 'http', # Esto indica que TokenAuthentication es un esquema de seguridad
                'scheme': 'bearer',
                'bearerFormat': 'Token', # Formato del token, opcional
            } # Esto indica que TokenAuthentication es un esquema de seguridad
        },
        #{
        #    'BasicAuth': {
        #          'type': 'http', # Esto indica que BasicAuthentication es un esquema de seguridad
        #          'scheme': 'basic',       
        # } # Para BasicAuthentication si lo habilitas
        #},
        {
            'SessionAuth': {
                'type': 'apiKey', 
                'in': 'header', # Indica que el token se envía en el header
                'name': 'sessionid', # Nombre del header para la sesión
            } # Para SessionAuthentication
        }
    ],
    # Si quieres que aparezca el campo de input del token:
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True, # Esto guarda el token en el navegador entre recargas
        'displayRequestDuration': True, # Muestra cuánto tarda la petición
    },
}


