from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=400)
    emoji = models.CharField(max_length=42, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.name}"

class OccurrenceManager(models.Manager):
    def get_queryset(self):
        # Override the default queryset to sort by timeofday in descending order when it's not null
        return super().get_queryset().order_by('-timeofday')

class Occurrence(models.Model):
    timestamp = models.DateField(default=timezone.now)
    timeofday = models.DateTimeField(null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=255, null=True)

    objects = OccurrenceManager()

    def __str__(self):
        return  f"{self.timestamp.strftime('%Y-%m-%d')}"