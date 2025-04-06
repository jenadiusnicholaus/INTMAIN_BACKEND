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
from django.utils import timezone


class LessonStatusViewSet(viewsets.ModelViewSet):
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

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.request.user

        # object, created = UserLearningLessonStatus.objects.get_or_create(
        #     user=user,
        #     program_module_week_lesson_id=self.request.query_params.get(
        #         "program_module_week_lesson_id"
        #     ),
        # )

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request_data = self.request.data
        status_value = request_data.get("status")
        pr_url = request_data.get("pr_url")
        pr_description = request_data.get("pr_description")
        is_to_be_reviewed = request_data.get("is_to_be_reviewed")

        data = {
            "status": status_value,
            "updated_at": timezone.now(),
            "updated_by": user.id,
        }

        if is_to_be_reviewed:
            data.update(
                {
                    "is_to_be_reviewed": True,
                    "pr_url": pr_url,
                    "pr_description": pr_description,
                }
            )

        serializer = UpdateUserLearningLessonStatusSerializer(
            data=data, instance=self.get_object(), partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
