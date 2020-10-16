from datetime import datetime, timedelta
import pytz
from django.db import models
# Create your models here.

class DateValidationError(Exception):
    """Raised when start_date of Event object is greater than end_date """
    pass


class EventQueryset(models.query.QuerySet):
    def created(self, user):
        return self.filter(created_by = user)

    def invited_to(self, user):
        event_ids = Invitation.objects.filter(receiver = user).values_list('event_id', flat=True)
        return self.filter(id__in=event_ids)

    def future_events(self, within_days):
        now = datetime.now(tz=pytz.timezone('Europe/Istanbul'))
        date_filter = now + timedelta(days=within_days)
        return self.filter(start_date__gte=now, end_date__lte= date_filter)


class Event(models.Model):
    created_by = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    objects = EventQueryset.as_manager()

    class Meta:
        unique_together = ('created_by', 'title', 'start_date')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise DateValidationError('start_date cannot be greater than end_date')
        super(Event, self).save(*args, **kwargs)



class Invitation(models.Model):
    receiver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='invitations')
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='invitations')
    will_attend = models.BooleanField(blank=True, null=True)