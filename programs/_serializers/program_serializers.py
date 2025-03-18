from authentication.serializers import GetUserSerializer
from menu_manager.models import MenuMeta
from programs._models.programs import ProgramMoreInfo, ProgramRating, ProgramStack
from programs._models.programs_modules import UserLearningLessonStatus
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


class GetMenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ["icon"]


class GetProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        depth = 1
        fields = "__all__"


class GetProgramDetailSerializer(serializers.ModelSerializer):
    stacks = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

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
        fields = "__all__"

    def get_modules(self, obj):
        modules = ProgramModule.objects.filter(program=obj)
        serializer = GetProgramModuleSerializer(modules, many=True)
        return serializer.data


class GetProgramStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramStack
        fields = ["name", "description"]


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


class GetProgramModuleWeekSerializer(serializers.ModelSerializer):
    meta = GetMenuMetaSerializer()

    class Meta:
        model = ProgramModuleWeek
        fields = ["id", "name", "display_name", "order", "meta", "description"]


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


class GetUserLearningLessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningLessonStatus
        fields = ["status"]


class CreateUserLearningLessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningLessonStatus
        fields = "__all__"


class CreateProgramFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFeedback
        fields = "__all__"
