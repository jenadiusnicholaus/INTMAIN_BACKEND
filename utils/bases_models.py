from django.db import models
from django.contrib.auth.models import User

# timezone
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


# class MenuMeta(models.Model):
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#     order = models.IntegerField(default=0)


# class Menu(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.CharField(max_length=255)
#     icon = models.CharField(max_length=255)
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#     order = models.IntegerField(default=0)
#     meta = models.ManyToManyField(MenuMeta)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.name
