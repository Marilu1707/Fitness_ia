import os
import sys
from pathlib import Path

# Ensure the project root is on the Python path so Django can locate the settings module.
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitness_crm.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
