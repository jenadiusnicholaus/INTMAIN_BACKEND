from django.urls import include, path
from rest_framework import routers
from .views import TutorProgramModelViewSet

router = routers.DefaultRouter()
router.register(r"program-vset", TutorProgramModelViewSet, basename="programs")


urlpatterns = [
    path("", include(router.urls)),
]
