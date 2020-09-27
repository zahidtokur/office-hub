from django.contrib import admin
from .models import Event
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'location', 'start_date')


admin.site.register(Event, EventAdmin)