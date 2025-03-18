# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers

from programs._views.programs_views import ProgramDetail
from .views import (
    ProgramList,
    UserEnrolledProgramList,
    ProgramModuleWeekList,
    UserLearningLesson,
    PrgrammerEnrollment,
    LessonStatusViewSet,
)


router = routers.DefaultRouter()
router.register(
    r"program-enrollment", PrgrammerEnrollment, basename="program-enrollment"
)
router.register(r"lesson-status", LessonStatusViewSet, basename="lesson-status")


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
    path(
        "program-detail/<int:pk>/",
        ProgramDetail.as_view(),
        name="program-detail",
    ),
]
