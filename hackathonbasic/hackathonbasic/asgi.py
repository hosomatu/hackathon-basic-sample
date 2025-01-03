# 非同期サーバーと連携するために使用するファイル
"""
ASGI config for hackathonbasic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathonbasic.settings')

application = get_asgi_application()
