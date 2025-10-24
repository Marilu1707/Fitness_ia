🧠 Fitness CRM con Inteligencia Artificial (Django)

Sistema web para alcanzar objetivos de entrenamiento: panel personalizado, rutinas automáticas (IA simulada), estadísticas y fotos de progreso.
Desarrollado con Django 5, HTML/CSS/JS (modo oscuro), SQLite, xhtml2pdf para reportes.

🚀 Funcionalidades

✅ Registro/Login de usuarios

👤 Perfil (edad, altura, peso, nivel)

🎯 Objetivos (tipo, peso deseado, días/semana)

📸 Fotos de progreso (media local)

📅 Historial (fecha, peso, horas entrenadas)

📈 Estadísticas: peso actual, diferencia, horas totales

🧠 Rutina personalizada (IA simulada en ia/generador.py)

📄 Descarga de reporte en PDF (en memoria)

🌙 Modo oscuro + estilo moderno

🧩 Tecnologías

Backend: Django 5.x

Frontend: HTML5 + CSS3 (dark), JavaScript ligero

Base de datos: SQLite (dev)

PDF: xhtml2pdf

Imágenes: Pillow

Control de versiones: Git/GitHub

📦 Requisitos

Python 3.11+

Pip

(Opcional) Git

⚙️ Instalación y ejecución (local)

Abrí una terminal en la carpeta del repositorio y seguí estos pasos.

Crear y activar entorno virtual (si no existe .venv/)

Windows (PowerShell)

python -m venv .venv
.\.venv\Scripts\activate


Linux / macOS

python3 -m venv .venv
source .venv/bin/activate


Instalar dependencias

pip install -r requirements.txt


Migraciones

python manage.py makemigrations
python manage.py migrate


(Opcional) Crear superusuario

python manage.py createsuperuser


Ejecutar el servidor

python manage.py runserver


Abrí: http://127.0.0.1:8000

🗂️ Estructura (resumen)
fitness_crm_ia/
├─ fitness_crm/           # settings.py, urls.py, wsgi.py
├─ usuarios/                 # modelos, vistas, forms, templates/usuarios/
├─ ia/
│  └─ generador.py           # lógica IA simulada
├─ templates/                # base.html, templates compartidos
│  └─ usuarios/              # dashboard.html, perfil.html, rutina.html, etc.
├─ static/
│  └─ css/styles.css         # modo oscuro
├─ media/                    # fotos de progreso (local)
├─ requirements.txt
└─ manage.py


Ajustá si tu estructura difiere, pero mantené manage.py, settings.py, urls.py, wsgi.py.

🔌 Configuración clave (settings)
LANGUAGE_CODE = "es-ar"  # o "es-es"
TIME_ZONE = "America/Argentina/Buenos_Aires"

STATIC_URL = "/static/"
# En desarrollo:
# STATICFILES_DIRS = [BASE_DIR / "static"]  # si usás carpeta global 'static'
# En despliegue clásico:
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


En urls.py (desarrollo) servir media si DEBUG es True:

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... tus rutas
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

🔍 Flujo de uso

Registrate o iniciá sesión.

Completá tu perfil (edad, altura, peso, nivel) y objetivos.

Cargá tus fotos de progreso y registrá tu historial (fecha, peso, horas).

Generá tu rutina personalizada (IA simulada).

Consultá estadísticas y descargá PDF del reporte.

🧪 Troubleshooting

404 en la raíz (/)

Verificá que en fitness_crm_ia/urls.py exista path("", home, name="home") y que la vista home esté implementada (p.ej., en core/views.py o dashboard de usuarios).

TemplateDoesNotExist

Confirmá TEMPLATES[0]['DIRS'] y que los archivos estén en templates/.

Asegurá {% load static %} en las plantillas que usan recursos estáticos.

Cargas de imágenes fallan

Verificá MEDIA_URL, MEDIA_ROOT y que estás sirviendo media en DEBUG.

Asegurá Pillow en requirements.txt.

PDF no se genera

Revisá que la vista use BytesIO y xhtml2pdf, y que los paths a CSS/estáticos sean resolubles en el contexto del template.

🧾 Licencia y autora

Proyecto de portfolio académico.
Autora: María Luján Massironi — 2025.
