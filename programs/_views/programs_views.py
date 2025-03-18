from rest_framework import views, status, generics, permissions
from rest_framework.response import Response

from programs._models.programs import UserEnrollmentProgram
from programs._models.programs_modules import ProgramModuleWeek, ProgramModuleWeekLesson
from programs._serializers.program_serializers import (
    CreateUserEnrollmentProgramSerializer,
    GetProgramDetailSerializer,
    GetProgramModuleWeekLessonSerializer,
    GetProgramModuleWeekSerializer,
    GetUserEnrollmentProgramSerializer,
)

from rest_framework import pagination

from ..models import Program
from ..serializers import GetProgramSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = GetProgramSerializer
    permission_classes = []

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = GetProgramDetailSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserEnrolledProgramList(generics.ListAPIView):
    serializer_class = GetUserEnrollmentProgramSerializer
    queryset = UserEnrollmentProgram.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset().filter(user=user).latest("created_at")
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class ProgramModuleWeekList(generics.ListAPIView):
    serializer_class = GetProgramModuleWeekSerializer
    queryset = ProgramModuleWeek.objects.all()

    def list(self, request, *args, **kwargs):
        program_module_id = self.request.query_params.get("program_module_id")
        if not program_module_id:
            return Response(
                {"massage": "program_module_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = (
            self.get_queryset()
            .filter(program_module_id=program_module_id)
            .order_by("order")
        )
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


# class CustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response(
#             {
#                 "links": {
#                     "next": self.get_next_link(),
#                     "previous": self.get_previous_link(),
#                 },
#                 "count": self.page.paginator.count,
#                 "results": data,
#             }
#         )


class UserLearningLesson(generics.ListAPIView):
    serializer_class = GetProgramModuleWeekLessonSerializer
    queryset = ProgramModuleWeekLesson.objects.all()

    def list(self, request, *args, **kwargs):
        week_id = self.request.query_params.get("week_id")
        if not week_id:
            return Response(
                {"massage": "week_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = (
            self.get_queryset().filter(program_module_week_id=week_id).order_by("order")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PrgrammerEnrollment(viewsets.ModelViewSet):
    serializer_class = GetUserEnrollmentProgramSerializer
    queryset = UserEnrollmentProgram.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset().filter(user=user).latest("created_at")
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # CreateUserEnrollmentProgramSerializer
        user_enrollment_program_data = {
            "user": request.user.id,
            "program": request.data.get("program_id"),
            "status": "pending",
            "progress_percentage": 0,
        }

        serializer = CreateUserEnrollmentProgramSerializer(
            data=user_enrollment_program_data
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_enrollment_program = serializer.save()

        return Response(
            {"message": "User enrolled in program successfully"},
            status=status.HTTP_201_CREATED,
        )


# class UpdateLessonLearnedStatus(generics.UpdateAPIView):
#     serializer_class = GetUserLearningLessonStatusSerializer
#     queryset = UserLearningLessonStatus.objects.all()
#     permission_classes = [IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         return Response(serializer.data)
