from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from rest_framework import routers

from auths.views import AuthViewSet, InternalViewSet

app_name = settings.APP_AUTH
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"auth", AuthViewSet, basename="Auth")
router.register(r"internal", InternalViewSet, basename="Internal")

urlpatterns = [
    url(r"^", include(router.urls)),
]
