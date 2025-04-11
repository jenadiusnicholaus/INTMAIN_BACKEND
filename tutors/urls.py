from django.urls import include, path
from rest_framework import routers
from .views import (
    ModuleWeekViewSet,
    TutorProgramModelViewSet,
    TutorProgramModuleViewSet,
    TutorProgramSubModuleLessonViewSet,
)

router = routers.DefaultRouter()
router.register(r"program-vset", TutorProgramModelViewSet, basename="programs")
router.register(
    r"program-module-vset", TutorProgramModuleViewSet, basename="program-modules"
)
router.register(
    r"program-module-week-vset", ModuleWeekViewSet, basename="program-module-weeks"
)
router.register(
    r"program-module-week-lesson-vset",
    TutorProgramSubModuleLessonViewSet,
    basename="program-module-week-lessons",
)


urlpatterns = [
    path("", include(router.urls)),
]
