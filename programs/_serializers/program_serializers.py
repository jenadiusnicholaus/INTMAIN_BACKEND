from authentication.serializers import GetUserSerializer
from ..models import Program, UserEnrollmentProgram
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

    class Meta:
        model = UserEnrollmentProgram
        fields = [
            "user_id",
            "program_name",
            "program_description",
            "program_image",
            "program_start_date",
            "program_end_date",
            "program_category",
            "status",
            "progress_percentage",
            "created_at",
            "updated_at",
        ]
