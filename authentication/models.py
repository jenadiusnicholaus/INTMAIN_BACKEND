from django.db import models
from django.contrib.auth.models import User

from utils.bases_models import BaseModel


class UserType(models.Model):
    TYPES = (
        ("STUDENT", "Student"),
        ("TEACHER", "Teacher"),
    )
    name = models.CharField(max_length=50, choices=TYPES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    user_type = models.ForeignKey(
        UserType, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.user.email


# Create your models here.
class VerificationCode(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_verification_code_set"
    )
    code = models.CharField(max_length=6, unique=True)
    otp_used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Verification Codes"
        ordering = ["-created_at"]
        unique_together = ["user", "code"]
