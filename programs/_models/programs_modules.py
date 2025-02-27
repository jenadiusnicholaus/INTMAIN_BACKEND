from utils.bases_models import BaseModel
from django.db import models
from markdownx.models import MarkdownxField
from ..models import Program

# User
from django.contrib.auth.models import User


class ProgramModule(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = MarkdownxField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("program", "name")
        ordering = ["order"]


class ProgramModuleWeek(BaseModel):
    program_module = models.ForeignKey(ProgramModule, on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("program_module", "week")
        ordering = ["week"]


class ProgramModuleWeekLesson(BaseModel):
    LEARNING_MODEL = (
        ("SOLO", "Solo"),
        ("GROUP", "Group"),
        ("HYBRID", "Hybrid"),
    )

    LESSION_TYPE = (
        ("NORMAL", "Normal"),
        ("QUIZ", "Quiz"),
        ("WEEKLY_CAPSTONE", "Weekly Capstone"),
        ("MIDTERM_CAPSTONE", "Midterm Capstone"),
        ("FINAL_CAPSTONE", "Final Capstone"),
    )

    program_module_week = models.ForeignKey(ProgramModuleWeek, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = MarkdownxField(blank=True, null=True)
    order = models.IntegerField(default=0)
    learning_model = models.CharField(
        max_length=40, choices=LEARNING_MODEL, default="SOLO"
    )
    lession_type = models.CharField(
        max_length=40, choices=LESSION_TYPE, default="NORMAL"
    )
    duration = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ("program_module_week", "name")
        ordering = ["order"]


class UserLearningLessonStatus(BaseModel):
    STATUS = (
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("SUBMITTED_FOR_REVIEW", "Submitted for Review"),
        ("REVIEWED_AND_APPROVED", "Reviewed and Approved"),
        ("REVIEWED_AND_REJECTED", "Reviewed and Rejected"),
        ("COMPLETED", "Completed"),
        ("SKIPPED", "Skipped"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program_module_week_lesson = models.ForeignKey(
        ProgramModuleWeekLesson, on_delete=models.CASCADE
    )
    status = models.CharField(max_length=40, choices=STATUS, default="NOT_STARTED")
