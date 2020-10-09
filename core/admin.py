from django.contrib import admin
from .models import User, UserSkill
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'job_title', 'registered_date')


class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill')


admin.site.register(User, UserAdmin)
admin.site.register(UserSkill, UserSkillAdmin)