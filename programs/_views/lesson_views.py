from rest_framework import viewsets

from programs._serializers.program_serializers import (
    UpdateUserLearningLessonStatusSerializer,
)
from ..serializers import GetUserLearningLessonStatusSerializer
from ..models import UserLearningLessonStatus
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class LessonStatusViewSet(generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    serializer_class = GetUserLearningLessonStatusSerializer
    queryset = UserLearningLessonStatus.objects.all()

    def get_object(self):
        user = self.request.user
        program_module_week_lesson = self.request.query_params.get(
            "program_module_week_lesson_id"
        )
        object, created = self.queryset.get_or_create(
            user=user,
            program_module_week_lesson_id=program_module_week_lesson,
            defaults={
                "status": "IN_PROGRESS",
                "created_at": datetime.now(),
                "created_by": user,
            },
        )
        return object

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        data = {
            "status": self.request.data.get("status"),
            "updated_at": datetime.now(),
            "updated_by": self.request.user.id,
        }
        serializer = UpdateUserLearningLessonStatusSerializer(
            data=data, instance=self.get_object(), partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
