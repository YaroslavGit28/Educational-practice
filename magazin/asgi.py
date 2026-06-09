"""
ASGI config for magazin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))
sys.path.insert(0, str(BASE_DIR / 'scripts'))

from load_env import load_env_file
load_env_file(BASE_DIR / '.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin.settings')

application = get_asgi_application()
