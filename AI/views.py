from django.shortcuts import render
from rest_framework import views
from .api import DeepSeekAPI
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

# Create your views here.


class AIsupport(views.APIView):
    def post(self, request):
        text = request.data["content"]
        api = DeepSeekAPI()
        content = api.get_response(text)
        return Response({"content": content})
