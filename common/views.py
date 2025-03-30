from django.shortcuts import render
from rest_framework import viewsets

from common.models import Stack
import requests
import json

from common.serializers import GetStackSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


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
