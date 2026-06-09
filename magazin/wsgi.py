import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))
sys.path.insert(0, str(BASE_DIR / 'scripts'))

from load_env import load_env_file
load_env_file(BASE_DIR / '.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin.settings')

application = get_wsgi_application()
