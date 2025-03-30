from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class PermissionHandler:
    @staticmethod
    def update_permissions(group_name, request, user, models):
        user = request.user if request.user.is_authenticated else user
        group, created = Group.objects.get_or_create(name=group_name)
        for model in models:
            content_type = ContentType.objects.get_for_model(model)

            # Filter permissions based on the model's content type
            permissions = Permission.objects.filter(content_type=content_type)

            # Add permission to group only if not already added
            if not group.permissions.filter(id__in=permissions).exists():
                group.permissions.add(*permissions)
                group.save()

            # Add same permission to user only if not already added
            if not user.user_permissions.filter(id__in=permissions).exists():
                user.user_permissions.add(*permissions)
                user.save()

            # Add group to user only if not already added
            if not user.groups.filter(name=group_name).exists():
                user.groups.add(group)
                user.save()
