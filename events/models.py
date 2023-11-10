from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_name = models.CharField(max_length=400)
    timestamp =  models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.event_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"