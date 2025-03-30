from django.db import models
from django.contrib.auth.models import User
from django_softdelete.models import SoftDeleteModel


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


class BaseSoftDeleteModel(SoftDeleteModel, models.Model):
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
