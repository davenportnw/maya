from django.contrib import admin

# Register your models here.
from .models import Event, Occurrence, CollaborationInvitation


admin.site.register(Event)
admin.site.register(Occurrence)
admin.site.register(CollaborationInvitation)
