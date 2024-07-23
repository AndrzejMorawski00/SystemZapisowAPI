from django.contrib import admin

from .models import UserPlan, UserSemester

# Register your models here.


admin.site.register(UserPlan)
admin.site.register(UserSemester)
