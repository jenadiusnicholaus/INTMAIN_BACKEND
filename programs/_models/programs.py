from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProgramCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="programs/images/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserEnrollmentProgram(models.Model):
    STATUS = (
        ("started", "Started"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.program.name}"


class ProgramFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} feedback for {self.program.name}"
