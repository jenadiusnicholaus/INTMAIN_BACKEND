# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include, path
from rest_framework import routers
from common.views import MenuMetaList, StacksViewset

router = routers.DefaultRouter()
router.register(r"stacks", StacksViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("menu_meta_data/", MenuMetaList.as_view()),
]
