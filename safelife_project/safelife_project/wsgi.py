"""
WSGI config for safelife_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safelife_project.settings')

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
application = get_wsgi_application()
sys.path.append('/safelife_project')
sys.path.append('safelife_project/safelife_project')
