from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser


class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.user_profile.user_type.name == "TEACHER"
            or request.user.groups.filter(name="TEACHER").exists()
        )


class IsTutorOrIsAdminUser(BasePermission):
    """
    Custom permission to allow access to tutors or admin users.
    """

    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view) and (
            IsTutor or IsAdminUser().has_permission(request, view)
        )
