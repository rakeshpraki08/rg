from django.urls import path

from .consumer import FetchComsumer

ws_urlpatterns = [
    
    path('ws/fetch-data/', FetchComsumer.as_asgi()),
]