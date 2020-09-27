from django.contrib import admin
from .models import Invitation
# Register your models here.

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'event', 'will_attend')


admin.site.register(Invitation, InvitationAdmin)