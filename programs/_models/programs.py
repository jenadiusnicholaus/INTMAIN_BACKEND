from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from common.models import Stack
from utils.bases_models import BaseModel
from markdownx.models import MarkdownxField


class ProgramCategory(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class BaseProgramPublication(BaseModel):
    PUB_STATUS = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    publication_status = models.CharField(
        max_length=10, default="draft", choices=PUB_STATUS
    )

    class Meta:
        abstract = True


class Program(BaseProgramPublication):
    LEVEL = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )
    # PUB_STATUS = (
    #     ("draft", "Draft"),
    #     ("published", "Published"),
    # )
    # publication_status = models.CharField(
    #     max_length=10, default="draft", choices=PUB_STATUS
    # )
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=200, choices=LEVEL, default="beginner")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="programs/images/", blank=True, null=True)

    def __str__(self):
        return self.name


class ProgramRating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} rating for {self.program.name}"


class ProgramMoreInfo(BaseModel):
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="more_info_set"
    )
    more_info = MarkdownxField()

    class Meta:
        verbose_name_plural = "Program More Info"

    def __str__(self):
        return self.program.name


class ProgramStack(BaseModel):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="program_stacks",
    )
    # name = models.CharField(max_length=200, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="program_stacks",
    )

    def __str__(self):
        return f"{self.program.name} - {self.name}"


class UserEnrollmentProgram(BaseModel):
    STATUS = (
        ("started", "Started"),
        ("pending", "Pending"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_enrollments"
    )
    progress_percentage = models.IntegerField(default=0)
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user", "program")

    def __str__(self):
        return f"{self.user.username} enrolled in {self.program.name}"


class ProgramFeedback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f"{self.user.username} feedback for {self.program.name}"
