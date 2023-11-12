from django.contrib import admin

# Register your models here.
from .models import Event, EventDetail

admin.site.register(Event)
admin.site.register(EventDetail)
