from authentication.serializers import (
    GetUserSerializer,
    GetUserWithPermissionsSerializer,
)
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


class GetMenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ["id", "icon"]


class GetProgramSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    created_by = GetUserWithPermissionsSerializer(read_only=True)

    class Meta:
        model = Program
        depth = 1
        fields = [
            "id",
            "level",
            "name",
            "description",
            "category_name",
            "image",
            "created_by",
        ]


class CreateProgramSerializer(serializers.ModelSerializer):
    image = Base64AnyFileField(required=True)

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
    class Meta:
        model = ProgramStack
        fields = ["name", "description"]


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
        fields = "__all__"


class GetProgramRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramRating
        fields = "__all__"


class GetProgramModuleWithOutSubModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModule
        fields = ["id", "name", "display_name", "order", "description"]


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

    class Meta:
        model = ProgramModuleWeek
        fields = ["id", "name", "display_name", "order", "meta", "description"]


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
    program_module_week_id = serializers.IntegerField(source="program_module_week.id")
    program_module_week_name = serializers.CharField(
        source="program_module_week.program_module.name"
    )
    # program_module_week_description = serializers.CharField(
    #     source="program_module_week.program_module.description"
    # )

    program_module_week_order = serializers.IntegerField(
        source="program_module_week.order"
    )
    name = serializers.CharField()
    description = serializers.CharField()
    order = serializers.IntegerField()
    learning_model = serializers.CharField(source="get_learning_model_display")
    lesson_type = serializers.CharField(source="get_lesson_type_display")
    duration = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_optional = serializers.BooleanField()
    formatted_markdown = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        status = obj.lesson_status.filter(user=self.context.get("request").user).first()
        sz = GetUserLearningLessonStatusSerializer(status)
        return sz.data["status"] if status else "NOT_STARTED"

    class Meta:
        model = ProgramModuleWeekLesson
        fields = "__all__"

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
