from django.shortcuts import render
from .models import Event, EventDetail
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    events = Event.objects.prefetch_related('eventdetail_set').all()
    return render(request, "landing/base.html", {'events': events})

def add_event(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        print('test')
        if event_name:
            event = Event.objects.create(
                name=event_name)
            EventDetail.objects.create(
                event=event, timestamp=timezone.now())
        return HttpResponseRedirect('/events/')
