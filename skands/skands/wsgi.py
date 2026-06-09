"""
WSGI config for skands project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skands.settings')

# Cela s'exécute une seule fois au démarrage de la fonction Serverless
if os.environ.get('VERCEL') == '1':
    from django.core.management import call_command
    try:
        print("Vercel détecté : Lancement automatique de collectstatic...")
        call_command('collectstatic', '--noinput', '--clear')
        print("Collectstatic terminé avec succès !")
    except Exception as e:
        print(f"Erreur lors du collectstatic automatique : {e}", file=sys.stderr)

application = get_wsgi_application()

app = application