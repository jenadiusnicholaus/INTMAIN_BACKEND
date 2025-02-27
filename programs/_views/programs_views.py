from rest_framework import views, status, generics, permissions
from rest_framework.response import Response

from ..models import Program
from ..serializers import GetProgramSerializer


class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = GetProgramSerializer
    permission_classes = []

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
