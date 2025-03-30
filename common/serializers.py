from rest_framework import serializers

from common.models import Stack


class GetStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = "__all__"
