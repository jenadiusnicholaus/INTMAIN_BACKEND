from django.contrib import admin
from ._models.programs import *
from ._models.programs_modules import *
from markdownx.admin import MarkdownxModelAdmin


# Register your models here.
admin.site.register(Program)
admin.site.register(ProgramCategory)
admin.site.register(UserEnrollmentProgram)
admin.site.register(ProgramFeedback)
admin.site.register(ProgramModule, MarkdownxModelAdmin)
admin.site.register(ProgramModuleWeek, MarkdownxModelAdmin)
admin.site.register(ProgramModuleWeekLesson, MarkdownxModelAdmin)
admin.site.register(UserLearningLessonStatus)
# admin.site.register(UserLearningModuleStatus)
