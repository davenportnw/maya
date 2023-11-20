from django.contrib import admin

# Register your models here.
from .models import Event, Occurrence

admin.site.register(Event)
admin.site.register(Occurrence)
