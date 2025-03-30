# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from authentication.views import (
    UserViewSet,
    RegisterView,
    ActivateAccountView,
    ResendOtpView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)


router = routers.DefaultRouter()
router.register(r"user", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(f"login/", TokenObtainPairView.as_view(), name="login"),
    path(f"token/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path(f"token/verify/", TokenVerifyView.as_view(), name="login_verify"),
    path(f"token/blacklist/", TokenBlacklistView.as_view(), name="login_blacklist"),
    path(f"register/", RegisterView.as_view(), name="register"),
    path(f"activate-account/", ActivateAccountView.as_view(), name="activate-account"),
    path(f"re-send-otp/", ResendOtpView.as_view(), name="re-send-otp"),
]
