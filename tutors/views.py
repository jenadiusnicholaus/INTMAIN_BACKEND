from rest_framework import viewsets

from authentication.utils import PermissionHandler
from programs._models.programs import Program
from programs._serializers.program_serializers import (
    CreateProgramDetailSerializer,
    CreateProgramSerializer,
    CreateProgramStackSerializer,
    GetProgramSerializer,
)
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsTutor
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import serializers


# Create your views here.
class TutorProgramModelViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = GetProgramSerializer
    permission_classes = [IsAuthenticated, IsTutor]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(created_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        # CreateProgramSerializer
        # CreateProgramDetailSerializer
        # CreateProgramStackSerializer

        program_data = {
            "name": request.data.get("name"),
            "category": request.data.get("category_id"),
            "created_by": request.user.id,
            "description": request.data.get("short_description"),
            "level": request.data.get("level"),
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "image": request.data.get("image"),
            "publication_status": request.data.get("publication_status"),
            "is_active": request.data.get("is_active"),
        }

        program_detail_data = {
            "program": None,
            "more_info": request.data.get("md_description"),
        }

        program_stacks = request.data.get("program_stacks")
        with transaction.atomic():
            program_serializer = CreateProgramSerializer(data=program_data)
            if not program_serializer.is_valid():
                raise serializers.ValidationError(program_serializer.errors)
            program = program_serializer.save()

            program_detail_data["program"] = program.id
            program_detail_serializer = CreateProgramDetailSerializer(
                data=program_detail_data
            )
            if not program_detail_serializer.is_valid():
                # delete parent
                program.delete()
                raise serializers.ValidationError(program_detail_serializer.errors)
            program_detail_serializer.save()

            for program_stack in program_stacks:
                program_stack_data = {
                    "program": program.id,
                    "stack": program_stack.get("stack_id"),
                }
                program_stack_serializer = CreateProgramStackSerializer(
                    data=program_stack_data
                )
                if not program_stack_serializer.is_valid():
                    # delete parent
                    program.delete()
                    raise serializers.ValidationError(program_stack_serializer.errors)
                program_stack_serializer.save()

            # update permissions
            try:

                PermissionHandler.update_permissions(
                    group_name="TEACHER",
                    user=request.user,
                    request=request,
                    models=[Program],
                )
            except Exception as e:
                # delete parent
                program.delete()
                raise serializers.ValidationError(f"Error updating permissions {e}")

        return Response(
            {"message": "Program created successfully", "program_id": program.id},
            status=status.HTTP_201_CREATED,
        )
