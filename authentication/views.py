from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from authentication.serializers import GetUserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
