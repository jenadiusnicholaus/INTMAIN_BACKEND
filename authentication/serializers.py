from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers


class GetUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]
