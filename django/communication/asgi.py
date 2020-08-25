import os

from core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication.settings')

application = get_asgi_application()
