from django.db import models


class Feedback(models.Model):
    created_by = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='feedback')
    title = models.CharField(max_length=50)
    message = models.TextField()
    is_anon = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('r', 'Request'),
        ('c', 'Complaint'),
        ('s', 'Suggestion'),
    ]
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
    )