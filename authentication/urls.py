# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from authentication.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(f"login/", TokenObtainPairView.as_view(), name="login"),
    path(f"token/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path(f"token/verify/", TokenVerifyView.as_view(), name="login_verify"),
    path(f"token/blacklist/", TokenBlacklistView.as_view(), name="login_blacklist"),
]
