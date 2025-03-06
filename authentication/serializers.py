from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class GetUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2", "email")

    def validate(self, attrs):
        """Ensure passwords match"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """Create a user instance"""
        user = User.objects.create(email=validated_data.get("email", ""))
        user.set_password(validated_data.get("password"))
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user
