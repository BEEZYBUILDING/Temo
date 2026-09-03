from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'plaster-lantern-bovine.ngrok-free.dev']

DJANGO_SETTINGS_MODULE = temo.settings.base

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://plaster-lantern-bovine.ngrok-free.dev",
]

CSRF_TRUSTED_ORIGINS = [
    "https://plaster-lantern-bovine.ngrok-free.dev",
]