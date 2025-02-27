from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="created_by_set"
    # )
    # updated_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="updated_by_set"
    # )

    class Meta:
        abstract = True
