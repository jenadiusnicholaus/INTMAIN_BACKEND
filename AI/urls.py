from django.urls import include, path
from rest_framework import routers
from .views import GetMCQSFromText


router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("get-mcqs-from-text/", GetMCQSFromText.as_view()),
]
