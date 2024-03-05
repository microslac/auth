from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from rest_framework import routers

from oauth2.views import Oauth2ViewSet

app_name = settings.APP_OAUTH2
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"^(?P<social_name>[-\w]+)", Oauth2ViewSet, basename="Oauth2")

urlpatterns = [
    url(r"^oauth2/", include(router.urls)),
]
