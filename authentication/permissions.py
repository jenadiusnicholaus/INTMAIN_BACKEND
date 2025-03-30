from rest_framework import permissions


class IsTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.user_profile.user_type.name == "TEACHER"
            or request.user.groups.filter(name="TEACHER").exists()
        )
