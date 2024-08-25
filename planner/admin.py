from django.contrib import admin

from .models import UserPlan, UserSemester

# Register your models here.

class UserPlanAdmin(admin.ModelAdmin):
    exclude = ('slug', )

admin.site.register(UserPlan, UserPlanAdmin)
admin.site.register(UserSemester)
