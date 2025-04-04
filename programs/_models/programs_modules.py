from menu_manager.models import MenuMeta
from payments.models import Packages, Payment
from programs._models.programs import BaseProgramPublication
from utils.bases_models import BaseModel
from django.db import models
from markdownx.models import MarkdownxField
from ..models import Program

from django.contrib.auth.models import User
from markdownx.utils import markdownify


class ProgramModule(BaseProgramPublication):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255, null=True, blank=True, default="program-module"
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)
    meta = models.ForeignKey(MenuMeta, on_delete=models.CASCADE, blank=True, null=True)
    description = MarkdownxField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        # unique_together = ("program", "name")
        ordering = ["order"]

    def __str__(self):
        return self.display_name or self.name


class ProgramModuleWeek(BaseProgramPublication):
    program_module = models.ForeignKey(ProgramModule, on_delete=models.CASCADE)
    week = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(
        max_length=255, null=True, blank=True, default="weekly-lessons"
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = MarkdownxField(blank=True, null=True)
    meta = models.ForeignKey(MenuMeta, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("program_module", "week")
        ordering = ["week"]
        verbose_name_plural = "Program Module Weeks"

    def __str__(self):
        return self.display_name or self.name


class ProgramModuleWeekLesson(BaseProgramPublication):
    LEARNING_MODEL = (
        ("SOLO", "Solo"),
        ("GROUP", "Group"),
        ("HYBRID", "Hybrid"),
    )

    LESSON_TYPE = (
        ("NORMAL", "Normal"),
        ("QUIZ", "Quiz"),
        ("WEEKLY_CAPSTONE", "Weekly Capstone"),
        ("MIDTERM_CAPSTONE", "Midterm Capstone"),
        ("FINAL_CAPSTONE", "Final Capstone"),
    )
    to_be_paid = models.BooleanField(default=False)
    program_module_week = models.ForeignKey(ProgramModuleWeek, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True)
    description = MarkdownxField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    learning_model = models.CharField(
        max_length=40, choices=LEARNING_MODEL, default="SOLO"
    )
    lesson_type = models.CharField(max_length=40, choices=LESSON_TYPE, default="NORMAL")
    duration = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ("program_module_week", "name")
        ordering = ["order"]

    def formatted_markdown(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name


# lesson payments
class ProgramPayment(BaseProgramPublication):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="program_payments"
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="program_payment_set"
    )

    class Meta:
        unique_together = ("program", "payment")

    def __str__(self):
        return f"{self.program.name} - {self.payment.user.first_name}"


class UserLearningLessonStatus(BaseProgramPublication):

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
        ProgramModuleWeekLesson, on_delete=models.CASCADE, related_name="lesson_status"
    )
    status = models.CharField(max_length=40, choices=STATUS, default="NOT_STARTED")
    is_to_be_reviewed = models.BooleanField(default=False)
    pr_url = models.URLField(blank=True, null=True)
    pr_description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "program_module_week_lesson")

    def __str__(self):
        return f"{self.user} - {self.program_module_week_lesson} - {self.status}"
