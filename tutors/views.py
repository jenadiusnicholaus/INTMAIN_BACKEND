from rest_framework import viewsets

from authentication.utils import PermissionHandler
from programs._models.programs import Program, ProgramMoreInfo, ProgramStack
from programs._models.programs_modules import (
    ProgramModule,
    ProgramModuleWeek,
    ProgramModuleWeekLesson,
)
from programs._serializers.program_serializers import (
    CreateProgramDetailSerializer,
    CreateProgramModuleSerializer,
    CreateProgramModuleWeekLessonSerializer,
    CreateProgramModuleWeekSerializer,
    CreateProgramSerializer,
    CreateProgramStackSerializer,
    GetProgramModuleWeekLessonSerializer,
    GetProgramModuleWeekSerializer,
    GetProgramModuleWithOutSubModulesSerializer,
    GetProgramSerializer,
    UpdateProgramDetailSerializer,
    UpdateProgramModuleSerializer,
    UpdateProgramModuleWeekLessonSerializer,
    UpdateProgramSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authentication.permissions import IsTutor, IsTutorOrIsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import serializers


# Create your views here.
class TutorProgramModelViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = GetProgramSerializer
    permission_classes = [IsAuthenticated, IsTutorOrIsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset().filter(created_by=request.user).order_by("-created_at")
        )
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
            "created_by": request.user.id,
        }

        program_detail_data = {
            "program": None,
            "more_info": request.data.get("md_description"),
            "created_by": request.user.id,
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
            {
                "message": "Program created successfully",
                "data": program_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        program_id = self.request.query_params.get("program_id")
        program = Program.objects.get(id=program_id)

        # Use the original values if not provided in the request
        program_data = {
            "name": request.data.get("name", program.name),
            "category": request.data.get("category_id", program.category.id),
            "updated_by": request.user.id,
            "description": request.data.get("short_description", program.description),
            "level": request.data.get("level", program.level),
            "start_date": request.data.get("start_date", program.start_date),
            "end_date": request.data.get("end_date", program.end_date),
            "publication_status": request.data.get(
                "publication_status", program.publication_status
            ),
            "is_active": request.data.get("is_active", program.is_active),
        }

        image = request.data.get("image")
        if image and image.strip():
            program_data["image"] = image

        stacks = request.data.get("program_stacks")

        with transaction.atomic():
            program_serializer = UpdateProgramSerializer(
                instance=program, data=program_data, partial=True
            )
            if not program_serializer.is_valid():
                raise serializers.ValidationError(program_serializer.errors)
            updated_program = program_serializer.save()

            program_detail = ProgramMoreInfo.objects.filter(program=program).update(
                more_info=request.data.get("md_description"),
                updated_by=request.user.id,
            )

            # upated if the stacks exist and add if not

            if len(stacks) > 0:
                for stack in stacks:
                    stack_obj, created = ProgramStack.objects.get_or_create(
                        stack_id=stack.get("stack_id"),
                        program_id=updated_program.id,
                    )

        return Response(
            {
                "message": "Program updated successfully",
                "data": program_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        program_id = self.request.query_params.get("program_id")
        try:
            program = Program.objects.get(id=program_id)
            program.delete()
            return Response(
                {
                    "message": "Program deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Program.DoesNotExist:
            raise serializers.ValidationError("Program does not exist")


class TutorProgramModuleViewSet(viewsets.ModelViewSet):
    queryset = ProgramModule.objects.all()
    serializer_class = GetProgramModuleWithOutSubModulesSerializer
    permission_classes = [IsAuthenticated, IsTutorOrIsAdminUser]

    def list(self, request, *args, **kwargs):
        program_id = self.request.query_params.get("program_id")
        queryset = self.get_queryset().filter(created_by=request.user)

        if program_id is not None:
            queryset = queryset.filter(program_id=program_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # CreateProgramModuleSerializer
        module_data = {
            "program": request.data.get("program_id"),
            "display_name": request.data.get("module_name"),
            "meta": request.data.get("meta_id"),
            "created_by": request.user.id,
            "publication_status": request.data.get("publication_status"),
            "description": request.data.get("md_description"),
            "order": request.data.get("order"),
            "created_by": request.user.id,
        }

        with transaction.atomic():
            module_serializer = CreateProgramModuleSerializer(data=module_data)
            if not module_serializer.is_valid():
                raise serializers.ValidationError(module_serializer.errors)
            module = module_serializer.save()

            # update permissions
            try:
                PermissionHandler.update_permissions(
                    group_name="TEACHER",
                    user=request.user,
                    request=request,
                    models=[ProgramModule],
                )
            except Exception as e:
                # delete parent
                module.delete()
                raise serializers.ValidationError(f"Error updating permissions {e}")

        return Response(
            {
                "message": "Module created successfully",
                "data": module_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        module_id = self.request.query_params.get("module_id")
        module = ProgramModule.objects.get(id=module_id)
        module_data = {
            "display_name": request.data.get("module_name", module.display_name),
            "meta": request.data.get("meta_id", module.meta.id),
            "publication_status": request.data.get(
                "publication_status", module.publication_status
            ),
            "description": request.data.get("md_description", module.description),
            "order": request.data.get("order", module.order),
            "updated_by": request.user.id,
        }

        with transaction.atomic():
            module_serializer = UpdateProgramModuleSerializer(
                instance=module, data=module_data, partial=True
            )
            if not module_serializer.is_valid():
                raise serializers.ValidationError(module_serializer.errors)
            module = module_serializer.save()

        return Response(
            {
                "message": "Module updated successfully",
                "data": module_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        module_id = self.request.query_params.get("module_id")
        try:
            module = ProgramModule.objects.get(id=module_id)
            module.delete()
            return Response(
                {
                    "message": "Module deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except ProgramModule.DoesNotExist:
            raise serializers.ValidationError("Module does not exist")


class ModuleWeekViewSet(viewsets.ModelViewSet):
    queryset = ProgramModuleWeek.objects.all()
    serializer_class = GetProgramModuleWeekSerializer

    def list(self, request, *args, **kwargs):
        module_id = self.request.query_params.get("module_id")
        queryset = self.get_queryset().filter(
            created_by=request.user,
        )

        if module_id is not None:
            queryset = queryset.filter(program_module_id=module_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # CreateProgramModuleSerializer
        sub_module_data = {
            "program_module": request.data.get("module_id"),
            "week": request.data.get("week"),
            "display_name": request.data.get("sub_module_name"),
            "meta": request.data.get("meta_id"),
            "created_by": request.user.id,
            "description": request.data.get("md_description"),
            "order": request.data.get("order"),
            "publication_status": request.data.get("publication_status"),
            "created_by": request.user.id,
        }
        with transaction.atomic():
            sub_module_serializer = CreateProgramModuleWeekSerializer(
                data=sub_module_data
            )
            if not sub_module_serializer.is_valid():
                raise serializers.ValidationError(sub_module_serializer.errors)
            sub_module = sub_module_serializer.save()

            # update permissions
            try:
                PermissionHandler.update_permissions(
                    group_name="TEACHER",
                    user=request.user,
                    request=request,
                    models=[ProgramModuleWeek],
                )
            except Exception as e:
                # delete parent
                sub_module.delete()
                raise serializers.ValidationError(f"Error updating permissions {e}")

        return Response(
            {
                "message": "Sub-module created successfully",
                "data": sub_module_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        sub_module_id = self.request.query_params.get("sub_module_id")
        sub_module = ProgramModuleWeek.objects.get(id=sub_module_id)
        sub_module_data = {
            "week": request.data.get("week", sub_module.week),
            "display_name": request.data.get(
                "sub_module_name", sub_module.display_name
            ),
            "meta": request.data.get("meta_id", sub_module.meta.id),
            "description": request.data.get("md_description", sub_module.description),
            "order": request.data.get("order", sub_module.order),
            "updated_by": request.user.id,
            "publication_status": request.data.get(
                "publication_status", sub_module.publication_status
            ),
        }

        with transaction.atomic():
            sub_module_serializer = CreateProgramModuleWeekSerializer(
                instance=sub_module, data=sub_module_data, partial=True
            )
            if not sub_module_serializer.is_valid():
                raise serializers.ValidationError(sub_module_serializer.errors)
            sub_module = sub_module_serializer.save()

        return Response(
            {
                "message": "Sub-module updated successfully",
                "data": sub_module_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        sub_module_id = self.request.query_params.get("sub_module_id")
        try:
            sub_module = ProgramModuleWeek.objects.get(id=sub_module_id)
            sub_module.delete()
            return Response(
                {
                    "message": "Sub-module deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except ProgramModuleWeek.DoesNotExist:
            raise serializers.ValidationError("Sub-module does not exist")


class TutorProgramSubModeleLessonViewSet(viewsets.ModelViewSet):
    queryset = ProgramModuleWeekLesson.objects.all()
    serializer_class = GetProgramModuleWeekLessonSerializer
    permission_classes = [IsAuthenticated, IsTutorOrIsAdminUser]

    def list(self, request, *args, **kwargs):
        sub_module_id = self.request.query_params.get("sub_module_id")
        queryset = (
            self.get_queryset()
            .filter(
                created_by=request.user,
            )
            .order_by("-created_at")
        )

        if sub_module_id is not None:
            queryset = queryset.filter(program_module_week_id=sub_module_id).order_by(
                -"created_at"
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # CreateProgramModuleSerializer
        lesson_data = {
            "program_module_week": request.data.get("sub_module_id"),
            "name": request.data.get("lesson_name"),
            "description": request.data.get("md_description"),
            "short_description": request.data.get("short_description"),
            "order": request.data.get("order"),
            "learning_model": request.data.get("learning_model"),
            "lesson_type": request.data.get("lesson_type"),
            "duration": request.data.get("duration"),
            "is_active": request.data.get("is_active"),
            "to_be_paid": request.data.get("to_be_paid"),
            "is_optional": request.data.get("is_optional"),
            "created_by": request.user.id,
            "publication_status": request.data.get("publication_status"),
        }
        with transaction.atomic():
            lesson_serializer = CreateProgramModuleWeekLessonSerializer(
                data=lesson_data
            )
            if not lesson_serializer.is_valid():
                raise serializers.ValidationError(lesson_serializer.errors)
            lesson = lesson_serializer.save()

            # update permissions
            try:
                PermissionHandler.update_permissions(
                    group_name="TEACHER",
                    user=request.user,
                    request=request,
                    models=[ProgramModuleWeekLesson],
                )
            except Exception as e:
                # delete parent
                lesson.delete()
                raise serializers.ValidationError(f"Error updating permissions {e}")

        return Response(
            {
                "message": "Lesson created successfully",
                "data": lesson_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        lesson_id = self.request.query_params.get("lesson_id")
        lesson = ProgramModuleWeekLesson.objects.get(id=lesson_id)
        lesson_data = {
            "name": request.data.get("lesson_name", lesson.name),
            "description": request.data.get("md_description", lesson.description),
            "short_description": request.data.get(
                "short_description", lesson.short_description
            ),
            "order": request.data.get("order", lesson.order),
            "learning_model": request.data.get("learning_model", lesson.learning_model),
            "lesson_type": request.data.get("lesson_type", lesson.lesson_type),
            "duration": request.data.get("duration", lesson.duration),
            "to_be_paid": request.data.get("to_be_paid", lesson.to_be_paid),
            "is_active": request.data.get("is_active", lesson.is_active),
            "is_optional": request.data.get("is_optional", lesson.is_optional),
            "updated_by": request.user.id,
            "publication_status": request.data.get(
                "publication_status", lesson.publication_status
            ),
        }

        with transaction.atomic():
            lesson_serializer = UpdateProgramModuleWeekLessonSerializer(
                instance=lesson, data=lesson_data, partial=True
            )
            if not lesson_serializer.is_valid():
                raise serializers.ValidationError(lesson_serializer.errors)
            lesson = lesson_serializer.save()

        return Response(
            {
                "message": "Lesson updated successfully",
                "data": lesson_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        lesson_id = self.request.query_params.get("lesson_id")
        try:
            lesson = ProgramModuleWeekLesson.objects.get(id=lesson_id)
            lesson.delete()
            return Response(
                {
                    "message": "Lesson deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except ProgramModuleWeekLesson.DoesNotExist:
            raise serializers.ValidationError("Lesson does not exist")
