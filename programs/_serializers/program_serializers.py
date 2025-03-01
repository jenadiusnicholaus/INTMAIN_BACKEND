from authentication.serializers import GetUserSerializer
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


class GetProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        depth = 1
        fields = "__all__"


class GetUserEnrollmentProgramSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    program_name = serializers.CharField(source="program.name")
    program_description = serializers.CharField(source="program.description")
    program_image = serializers.ImageField(source="program.image")
    program_start_date = serializers.DateField(source="program.start_date")
    program_end_date = serializers.DateField(source="program.end_date")
    program_category = serializers.CharField(source="program.category.name")
    status = serializers.CharField(source="get_status_display")
    progress_percentage = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    modules = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrollmentProgram
        fields = "__all__"

    def get_modules(self, obj):
        module = ProgramModule.objects.filter(program=obj.program)
        serializer = GetProgramModuleSerializer(module, many=True)
        return serializer.data


class GetProgramCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCategory
        fields = "__all__"


class GetProgramModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModule
        fields = "__all__"


class GetProgramModuleWeekSerializer(serializers.ModelSerializer):
    week_lessons = serializers.SerializerMethodField()

    class Meta:
        model = ProgramModuleWeek
        fields = "__all__"

    def get_week_lessons(self, obj):
        week_lessons = ProgramModuleWeekLesson.objects.filter(
            program_module_week=obj.id
        )
        serializer = GetProgramModuleWeekLessonSerializer(week_lessons, many=True)
        return serializer.data


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
        return obj.formatted_markdown()
