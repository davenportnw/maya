from django.shortcuts import render
from .models import Event, EventDetail


# Create your views here.
def index(request):
    events = Event.objects.prefetch_related('eventdetail_set').all()
    return render(request, "landing/base.html", {'events': events})

