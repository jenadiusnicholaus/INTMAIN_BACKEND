# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from .views import ProgramList, UserEnrolledProgramList


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("program-list/", ProgramList.as_view(), name="program-list"),
    path(
        "user-enrolled-program-list/",
        UserEnrolledProgramList.as_view(),
        name="user-enrolled-program-list",
    ),
]
