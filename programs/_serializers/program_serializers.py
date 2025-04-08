from authentication.serializers import (
    GetUserSerializer,
    GetUserWithPermissionsSerializer,
)
from common.serializers import GetStackSerializer
from menu_manager.models import MenuMeta
from programs._models.programs import ProgramMoreInfo, ProgramRating, ProgramStack
from programs._models.programs_modules import UserLearningLessonStatus
from utils.any_base_64_file_helper import Base64AnyFileField
from ..models import (
    Program,
    UserEnrollmentProgram,
    ProgramCategory,
    ProgramModule,
    ProgramModuleWeek,
    ProgramFeedback,
    ProgramModuleWeekLesson,
)
from rest_framework import serializers
from django.db import models
from drf_extra_fields.fields import Base64FileField

# user
from django.contrib.auth.models import User


class GetMenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ["id", "icon"]


class GetProgramSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    created_by = GetUserWithPermissionsSerializer(read_only=True)
    stacks = serializers.SerializerMethodField()
    publication_status = serializers.SerializerMethodField()
    detailed_description = serializers.SerializerMethodField()

    def get_publication_status(self, obj):
        return obj.unpackpublication_status()

    def get_category(self, obj):
        serializer = GetProgramCategorySerializer(obj.category)
        return serializer.data

    def get_stacks(self, obj):
        stacks = obj.program_stacks.all()
        serializer = GetProgramStackSerializer(stacks, many=True)
        return serializer.data

    def get_detailed_description(self, obj):

        more_info = obj.more_info_set.filter().first()
        serializer = GetProgramMoreInfoSerializer(more_info)
        return serializer.data["more_info"]

    class Meta:
        model = Program
        depth = 1
        fields = [
            "id",
            "level",
            "name",
            "description",
            "category",
            "image",
            "stacks",
            "created_by",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
            "publication_status",
            "detailed_description",
        ]


class CreateProgramSerializer(serializers.ModelSerializer):
    image = Base64AnyFileField(required=True)

    class Meta:
        model = Program
        fields = "__all__"


class UpdateProgramSerializer(serializers.ModelSerializer):
    image = Base64AnyFileField(required=False)

    class Meta:
        model = Program
        fields = "__all__"


class GetProgramDetailSerializer(serializers.ModelSerializer):
    stacks = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    level = serializers.CharField(source="get_level_display")

    def get_details(self, obj):
        more_info = obj.more_info_set.filter().first()
        serializer = GetProgramMoreInfoSerializer(more_info)
        return serializer.data["more_info"]

    def get_stacks(self, obj):
        stacks = obj.program_stacks.all()
        serializer = GetProgramStackSerializer(stacks, many=True)
        return serializer.data

    def get_rating(self, obj):
        return (
            obj.ratings.all().aggregate(models.Avg("rating"))["rating__avg"]
            if obj.ratings.all().exists()
            else 0.0
        )

    class Meta:
        model = Program

        exclude = (
            "description",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        )

    def get_modules(self, obj):

        modules = ProgramModule.objects.filter(program=obj.id).order_by("order").first()
        serializer = GetDUserEnrollmentProgramSerializer(
            modules,
        )
        return serializer.data.get("modules")


class CreateProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMoreInfo
        fields = "__all__"


class UpdateProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMoreInfo
        fields = "__all__"


class GetProgramStackSerializer(serializers.ModelSerializer):
    stacks = serializers.SerializerMethodField()

    def get_stacks(self, obj):
        serializer = GetStackSerializer(obj.stack)
        return serializer.data

    class Meta:
        model = ProgramStack
        fields = ["id", "stacks"]


class CreateProgramStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramStack
        fields = "__all__"


class GetProgramMoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMoreInfo
        fields = "__all__"


class GetUserEnrollmentProgramSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrollmentProgram
        fields = ["modules"]

    def get_modules(self, obj):
        module = ProgramModule.objects.filter(program=obj.program)
        serializer = GetProgramModuleSerializer(module, many=True)
        return serializer.data


class StatsSerializer(serializers.ModelSerializer):
    # Enrolled Programs
    enrolled_programs = serializers.SerializerMethodField()

    # Completed Programs
    completed_programs = serializers.SerializerMethodField()

    # Pending Programs
    pending_programs = serializers.SerializerMethodField()

    # Earn Certificate
    earned_certificate = serializers.SerializerMethodField()

    current_enrolled_program = serializers.SerializerMethodField()

    def get_enrolled_programs(self, obj):
        total_enrolled_programs = UserEnrollmentProgram.objects.filter(user=obj.id)

        return total_enrolled_programs.count()

    def get_completed_programs(self, obj):
        total_completed_programs = UserEnrollmentProgram.objects.filter(
            user=obj.id,
        )
        completed_programs = 0

        for program in total_completed_programs:
            total_lessons = ProgramModuleWeekLesson.objects.filter(
                program_module_week__program_module__program=program.program
            ).count()
            completed_lessons = UserLearningLessonStatus.objects.filter(
                user=obj.id,
                program_module_week_lesson__program_module_week__program_module__program=program.program,
                status="COMPLETED",
            ).count()

            # calculate percentage
            # if all lessons are completed then percentage is 100    and program si done
            if total_lessons == completed_lessons:
                completed_programs += 1
            else:
                completed_percentage = int((completed_lessons / total_lessons) * 100)
                if completed_percentage >= 100:
                    completed_programs += 1

            return completed_programs

        return completed_programs

    def get_pending_programs(self, obj):
        return 0

    def get_earned_certificate(self, obj):
        return 0

    def get_current_enrolled_program(self, obj):
        current_percentage = 0
        total_percentage = 0
        completed_lessons = 0

        try:
            current_enrolled_program = UserEnrollmentProgram.objects.filter(
                user=obj.id,
            ).latest("created_at")
        except UserEnrollmentProgram.DoesNotExist:
            return {
                "total_percentage": total_percentage,
                "completed_lessons": completed_lessons,
                "total_lessons": 0,
                "total_sub_modules": 0,
            }

        current_enrolled_program_all_modules = ProgramModule.objects.filter(
            program=current_enrolled_program.program,
        )
        total_sub_modules = 0

        total_sub_modules = ProgramModuleWeek.objects.filter(
            program_module__program=current_enrolled_program.program
        ).count()

        total_lessons = ProgramModuleWeekLesson.objects.filter(
            program_module_week__program_module__program=current_enrolled_program.program
        ).count()

        completed_lessons = UserLearningLessonStatus.objects.filter(
            user=obj.id,
            program_module_week_lesson__program_module_week__program_module__program=current_enrolled_program.program,
            status="COMPLETED",
        ).count()

        if total_lessons > 0:
            current_percentage = int((completed_lessons / total_lessons) * 100)

        return {
            "current_percentage": current_percentage,
            "total_percentage": total_percentage,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "total_sub_modules": total_sub_modules,
            "program_name": current_enrolled_program.program.name,
            "program_id": current_enrolled_program.program.id,
            "program_image": current_enrolled_program.program.image.url,
            "program_description": current_enrolled_program.program.description,
        }

    class Meta:
        model = User
        fields = [
            "enrolled_programs",
            "completed_programs",
            "pending_programs",
            "earned_certificate",
            "current_enrolled_program",
        ]


class GetDUserEnrollmentProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for UserEnrollmentProgram with modules as ProgramModule
    """

    modules = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrollmentProgram
        fields = ["modules"]

    def get_modules(self, obj):
        module = ProgramModule.objects.filter(program=obj.program)
        serializer = GetDProgramModuleSerializer(module, many=True)
        return serializer.data


class CreateUserEnrollmentProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrollmentProgram
        fields = "__all__"


class GetProgramCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCategory
        # fields = "__all__"

        # "created_by": null,
        # "updated_by": null,
        # "deleted_by": null

        exclude = (
            "description",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        )


class GetProgramRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramRating
        fields = "__all__"


class GetProgramModuleWithOutSubModulesSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name")
    meta = GetMenuMetaSerializer()
    # publication_status = serializers.SerializerMethodField()

    # def get_publication_status(self, obj):
    #     return obj.program.unpackpublication_status()

    class Meta:
        model = ProgramModule
        fields = [
            "id",
            "program_id",
            "program_name",
            "name",
            "display_name",
            "order",
            "description",
            "meta",
            "publication_status",
        ]


class GetProgramModuleSerializer(serializers.ModelSerializer):

    # children are module weeks

    children = serializers.SerializerMethodField()
    meta = GetMenuMetaSerializer()

    class Meta:
        model = ProgramModule
        fields = [
            "id",
            "name",
            "display_name",
            "order",
            "children",
            "meta",
            "description",
        ]

    def get_children(self, obj):
        children = ProgramModuleWeek.objects.filter(program_module=obj.id).order_by(
            "order"
        )
        serializer = GetProgramModuleWeekSerializer(children, many=True)
        return serializer.data


# redant Serializer for ProgramModuleWeekLesson
class GetDProgramModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for ProgramModule with children as ProgramModuleWeek
    D is program Details
    """

    # children are module weeks

    children = serializers.SerializerMethodField()
    meta = GetMenuMetaSerializer()

    class Meta:
        model = ProgramModule
        fields = [
            "id",
            "name",
            "display_name",
            "description",
            "order",
            "children",
            "meta",
        ]

    def get_children(self, obj):
        children = ProgramModuleWeek.objects.filter(program_module=obj.id).order_by(
            "order"
        )
        serializer = GetDProgramModuleWeekSerializer(children, many=True)
        return serializer.data


class CreateProgramModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModule
        fields = "__all__"


class UpdateProgramModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModule
        fields = "__all__"


class GetDProgramModuleWeekSerializer(serializers.ModelSerializer):
    """
    Serializer for ProgramModuleWeek with children as ProgramModuleWeekLesson"""

    meta = GetMenuMetaSerializer()

    class Meta:
        model = ProgramModuleWeek
        fields = [
            "id",
            "name",
            "display_name",
            "order",
            "meta",
        ]


class GetProgramModuleWeekSerializer(serializers.ModelSerializer):
    meta = GetMenuMetaSerializer()
    program_module_id = serializers.IntegerField(source="program_module.id")
    program_module_name = serializers.CharField(source="program_module.display_name")

    class Meta:
        model = ProgramModuleWeek
        fields = [
            "id",
            "name",
            "display_name",
            "order",
            "meta",
            "description",
            "publication_status",
            "program_module_id",
            "program_module_name",
        ]


class CreateProgramModuleWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModuleWeek
        fields = "__all__"


class GetProgramFeedbackSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    program_name = serializers.CharField(source="program.name")
    feedback = serializers.CharField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ProgramFeedback
        fields = "__all__"


class GetProgramModuleWeekLessonSerializer(serializers.ModelSerializer):
    # program_module_week_id = serializers.IntegerField(source="program_module_week.id")
    # program_module_week_name = serializers.CharField(
    #     source="program_module_week.program_module.name"
    # )
    # program_module_week_description = serializers.CharField(
    #     source="program_module_week.program_module.description"
    # )

    # program_module_week_order = serializers.IntegerField(
    #     source="program_module_week.order"
    # )
    name = serializers.CharField()
    description = serializers.CharField()
    order = serializers.IntegerField()
    learning_model = serializers.CharField()
    lesson_type = serializers.CharField()
    duration = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_optional = serializers.BooleanField()
    formatted_markdown = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    sub_module_name = serializers.CharField(source="program_module_week.display_name")
    sub_module_id = serializers.IntegerField(source="program_module_week.id")

    def get_status(self, obj):
        status = obj.lesson_status.filter(user=self.context.get("request").user).first()
        sz = GetUserLearningLessonStatusSerializer(status)
        return sz.data["status"] if status else "NOT_STARTED"

    class Meta:
        model = ProgramModuleWeekLesson
        fields = [
            "id",
            "name",
            "description",
            "order",
            "learning_model",
            "lesson_type",
            "duration",
            "is_active",
            "is_optional",
            "formatted_markdown",
            "status",
            "sub_module_name",
            "sub_module_id",
            "created_at",
            "updated_at",
            "created_by",
            "publication_status",
            "short_description",
        ]

    def get_formatted_markdown(self, obj):
        request = self.context.get("request")
        if request:
            # Replace relative URLs with absolute URLs
            base_url = request.build_absolute_uri("/")
            formatted_markdown = obj.formatted_markdown().replace(
                "/media/", f"{base_url}media/"
            )
            return formatted_markdown
        return obj.formatted_markdown

    # update description media urls to absolute urls
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            # Replace relative URLs with absolute URLs
            base_url = request.build_absolute_uri("/")
            data["description"] = data["description"].replace(
                "/media/", f"{base_url}media/"
            )
        return data


class CreateProgramModuleWeekLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModuleWeekLesson
        fields = "__all__"


class UpdateProgramModuleWeekLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModuleWeekLesson
        fields = "__all__"


class GetUserLearningLessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningLessonStatus
        fields = ["status"]


class CreateUserLearningLessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningLessonStatus
        fields = "__all__"


class UpdateUserLearningLessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningLessonStatus
        fields = "__all__"


class CreateProgramFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFeedback
        fields = "__all__"
