# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
