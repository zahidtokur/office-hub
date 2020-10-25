from django.contrib import admin
from .models import Event, Invitation, Comment
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'location', 'start_date')


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'event', 'will_attend')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'event', 'created_at')


admin.site.register(Event, EventAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Comment, CommentAdmin)