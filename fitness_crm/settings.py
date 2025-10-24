import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "clave-insegura-por-defecto")
def get_env_list(var_name: str, default: list[str]) -> list[str]:
    """Return a cleaned list of values from a comma-separated environment variable."""

    value = os.getenv(var_name)
    if value:
        return [item.strip() for item in value.split(",") if item.strip()]
    return default


DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in {"true", "1", "yes"}

DEFAULT_ALLOWED_HOSTS = [
    "fitness-crm-ia.vercel.app",
    "127.0.0.1",
    "localhost",
]
ALLOWED_HOSTS = get_env_list("DJANGO_ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS)

DEFAULT_CSRF_TRUSTED_ORIGINS = [
    "https://fitness-crm-ia.vercel.app",
    "https://*.vercel.app",
    "http://localhost",
    "http://127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = get_env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS", DEFAULT_CSRF_TRUSTED_ORIGINS
)

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',  # tu app principal
    'crispy_forms',
    'crispy_bootstrap5',
]

# Configuración de crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs raíz
ROOT_URLCONF = 'fitness_crm.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'fitness_crm.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Validadores de contraseña (pueden personalizarse luego)
AUTH_PASSWORD_VALIDATORS = []

# Internacionalización
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# Archivos multimedia (fotos, PDFs, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Modelo de ID por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones post-login
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'index'

