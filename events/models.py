from django.db import models
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=400)
    def __str__(self):
        return f"{self.name}"

class Occurrence(models.Model):
    timestamp =  models.DateField(default=timezone.now)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return  f"{self.timestamp.strftime('%Y-%m-%d')}"