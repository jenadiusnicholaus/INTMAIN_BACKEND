from django.shortcuts import render
from rest_framework import viewsets

from authentication.serializers import GetUserSerializer
from common.models import Stack
import requests
import json

from common.serializers import GetStackSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics

from menu_manager.models import MenuMeta
from programs._models.programs import ProgramCategory, UserEnrollmentProgram
from programs._serializers.program_serializers import (
    GetMenuMetaSerializer,
    GetProgramCategorySerializer,
    StatsSerializer,
)
from django.contrib.auth.models import User


class StatsView(generics.RetrieveAPIView):
    serializer_class = StatsSerializer
    queryset = User.objects.all()
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.request.user,
        )
        return Response(serializer.data)


class MenuMetaList(generics.ListAPIView):
    serializer_class = GetMenuMetaSerializer
    queryset = MenuMeta.objects.all()
    permission_classes = []

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset().filter(), many=True)
        return Response(serializer.data)


class StacksViewset(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    permission_classes = []
    serializer_class = GetStackSerializer

    def list(self, request, *args, **kwargs):
        piston_api_base_url = "https://emkc.org/api/v2/piston/runtimes"
        # make request to piston api to get list of runtimes
        try:
            response = requests.get(piston_api_base_url)
            runtimes = json.loads(response.content)
            # create list of Stack objects from runtimes
            #  save if not exists
        except Exception as e:
            raise serializers.ValidationError(
                {"error": "Unable to fetch runtimes from Piston API"}
            )
        for runtime in runtimes:
            stack, created = Stack.objects.update_or_create(
                name=runtime["language"], version=runtime["version"]
            )

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


class CategoriesViewset(viewsets.ModelViewSet):
    queryset = ProgramCategory.objects.all()
    permission_classes = []
    serializer_class = GetProgramCategorySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)
