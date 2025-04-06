from django.urls import include, path
from rest_framework import routers
from .views import AIsupport


router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("ai-support/", AIsupport.as_view()),
]
