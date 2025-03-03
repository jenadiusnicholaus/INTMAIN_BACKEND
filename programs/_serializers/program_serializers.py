from authentication.serializers import GetUserSerializer
from menu_manager.models import MenuMeta
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


class GetMenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ["icon"]


class GetProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        depth = 1
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


class GetProgramCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCategory
        fields = "__all__"


class GetProgramModuleSerializer(serializers.ModelSerializer):

    # children are module weeks

    children = serializers.SerializerMethodField()
    meta = GetMenuMetaSerializer()

    class Meta:
        model = ProgramModule
        fields = ["id", "name", "display_name", "order", "children", "meta"]

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
        fields = ["id", "name", "display_name", "order", "meta"]


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
    program_module_week_order = serializers.IntegerField(
        source="program_module_week.order"
    )
    name = serializers.CharField()
    description = serializers.CharField()
    order = serializers.IntegerField()
    learning_model = serializers.CharField(source="get_learning_model_display")
    lession_type = serializers.CharField(source="get_lession_type_display")
    duration = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_optional = serializers.BooleanField()
    formatted_markdown = serializers.SerializerMethodField()

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
