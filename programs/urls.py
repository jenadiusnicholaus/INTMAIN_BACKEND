# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from .views import (
    ProgramList,
    UserEnrolledProgramList,
    ProgramModuleWeekList,
    UserLearningLesson,
)


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("program-list/", ProgramList.as_view(), name="program-list"),
    path(
        "user-enrolled-program-list/",
        UserEnrolledProgramList.as_view(),
        name="user-enrolled-program-list",
    ),
    path(
        "program-module-week-list/",
        ProgramModuleWeekList.as_view(),
        name="program-module-week-list",
    ),
    path(
        "user-learning-lesson-list/",
        UserLearningLesson.as_view(),
        name="user-learning-lesson",
    ),
]
