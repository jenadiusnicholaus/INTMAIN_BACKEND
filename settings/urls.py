"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from markdownx import urls as markdownx

SUFFIX = f"api/{settings.API_VERSION}"

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add your URL patterns here
    path(f"{SUFFIX}/authentication/", include("authentication.urls")),
    # programs
    path(f"{SUFFIX}/programs/", include("programs.urls")),
    path(f"{SUFFIX}/AI/", include("AI.urls")),
    path("markdownx/", include(markdownx)),
    path("mdeditor/", include("mdeditor.urls")),
    path(f"{SUFFIX}/menu_manager/", include("menu_manager.urls")),
    path(f"{SUFFIX}/common/", include("common.urls")),
    path(f"{SUFFIX}/payments/", include("payments.urls")),
    path(f"{SUFFIX}/tutors/", include("tutors.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
