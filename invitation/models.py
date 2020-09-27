from django.db import models

# Create your models here.


class Invitation(models.Model):
    receiver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='invitations')
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE,related_name='invitations')
    will_attend = models.BooleanField(blank=True, null=True)
