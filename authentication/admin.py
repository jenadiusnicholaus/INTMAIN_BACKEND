from django.contrib import admin
from .models import VerificationCode, UserProfile, UserType

# Register your models here.
admin.site.register(VerificationCode)
admin.site.register(UserProfile)
admin.site.register(UserType)
