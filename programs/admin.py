from django.contrib import admin
from ._models.programs import *
from ._models.programs_modules import *

# Register your models here.
admin.site.register(Program)
admin.site.register(ProgramCategory)
admin.site.register(UserEnrollmentProgram)
admin.site.register(ProgramFeedback)
admin.site.register(ProgramModule)
admin.site.register(ProgramModuleWeek)
admin.site.register(ProgramModuleWeekLesson)
admin.site.register(UserLearningLessonStatus)
# admin.site.register(UserLearningModuleStatus)
# admin.site.register(UserLearningProgramStatus)
