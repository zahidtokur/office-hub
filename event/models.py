from django.db import models

# Create your models here.


class Event(models.Model):
    created_by = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        unique_together = ('created_by', 'title', 'start_date')

    def __str__(self):
        return self.title
