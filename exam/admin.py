from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Section)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.StudentDetails)
admin.site.register(models.Examination)