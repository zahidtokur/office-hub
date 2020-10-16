from django.contrib import admin
from .models import Event, Invitation
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'location', 'start_date')


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'event', 'will_attend')


admin.site.register(Event, EventAdmin)
admin.site.register(Invitation, InvitationAdmin)