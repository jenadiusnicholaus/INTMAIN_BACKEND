from rest_framework import views, status, generics, permissions
from rest_framework.response import Response

from programs._models.programs import UserEnrollmentProgram
from programs._models.programs_modules import ProgramModuleWeek
from programs._serializers.program_serializers import (
    GetProgramModuleWeekSerializer,
    GetUserEnrollmentProgramSerializer,
)

from ..models import Program
from ..serializers import GetProgramSerializer
from rest_framework.permissions import IsAuthenticated


class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = GetProgramSerializer
    permission_classes = []

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserEnrolledProgramList(generics.ListAPIView):
    serializer_class = GetUserEnrollmentProgramSerializer
    queryset = UserEnrollmentProgram.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class ProgramModuleWeekList(generics.ListAPIView):
    serializer_class = GetProgramModuleWeekSerializer
    queryset = ProgramModuleWeek.objects.all()

    def list(self, request, *args, **kwargs):
        program_module_id = self.kwargs.get("program_module_id")
        queryset = self.get_queryset().filter(program_module_id=program_module_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
