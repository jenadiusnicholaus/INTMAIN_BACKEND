from ..models import Program
from rest_framework import serializers


class GetProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"
