"""
WSGI config for arc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arc.settings")
sys.stderr.write('ok2')
try:
  sys.stderr.write('ok here')
  application = get_wsgi_application()
except Exception as e:
  sys.stderr.write(str(e))
  if 'mod_wsgi' in sys.modules:
    traceback.print_exc()
