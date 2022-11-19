"""
ASGI config for rg project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# from query_app.routing import ws_urlpatterns

# from channels.auth import AuthMiddlewareStack



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rg.settings')

# application = ProtocolTypeRouter({
#     'http' : get_asgi_application(),
#     'websocket' : AuthMiddlewareStack(URLRouter(ws_urlpatterns))
# })

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rg.settings')
django.setup()

from channels.auth import AuthMiddleware, AuthMiddlewareStack
from query_app.routing import ws_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ws_urlpatterns
        )
    )
})


