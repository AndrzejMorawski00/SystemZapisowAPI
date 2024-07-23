from django.contrib import admin
from .models import Semester, CourseEffect, CourseTag, CourseType, Course
# Register your models here.


class SemesterAdmin(admin.ModelAdmin):
    exclude = ('slug', )



admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course)
admin.site.register(CourseTag)
admin.site.register(CourseType)
admin.site.register(CourseEffect)
