from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from authentication.models import UserProfile


class GetUserWithPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
        ]


class GetUserSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = serializers.CharField(
        source="user_profile.phone_number", read_only=True
    )
    profile_picture = serializers.ImageField(
        source="user_profile.profile_picture", read_only=True
    )
    user_type = serializers.CharField(
        source="user_profile.user_type.name", read_only=True
    )
    # permissions = serializers.SerializerMethodField()

    user_groups = serializers.SerializerMethodField()

    # group_permissions = serializers.SerializerMethodField()

    def get_user_groups(self, obj):
        """Get all groups of user"""
        groups = obj.groups.all()
        # make group name the uppercase
        groups = [group.name.upper() for group in groups]
        return groups

    def get_group_permissions(self, obj):
        """Get all group permissions of user"""
        group_permissions = []
        for group in obj.groups.all():
            group_permissions += list(group.permissions.all())
        # make code name the uppercase
        group_permissions = [
            permission.codename.upper() for permission in group_permissions
        ]
        return group_permissions

    def get_permissions(self, obj):
        """Get all permissions of user"""
        permissions = obj.user_permissions.all()
        # make code name the uppercase
        permissions = [permission.codename.upper() for permission in permissions]
        return permissions

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "phone_number",
            "user_type",
            "user_groups",
            "date_joined",
            "profile_picture",
            # "group_permissions",
            # "permissions",
        ]


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
        fields = (
            "password",
            "password2",
            "email",
            "username",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        """Ensure passwords match"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=False,
            is_staff=False,
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class CreateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
