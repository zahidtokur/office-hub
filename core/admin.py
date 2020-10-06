from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'job_title', 'registered_date')


admin.site.register(User, UserAdmin)