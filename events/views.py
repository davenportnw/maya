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
        event_name = request.POST.get('event_name').strip()

        if event_name:
            # Try to get an event with a case-insensitive match
            event = Event.objects.filter(name__iexact=event_name).first()

            # If event does not exist, create a new one
            if not event:
                event = Event.objects.create(name=event_name)

            # Create a new EventDetail for this event
            EventDetail.objects.create(event=event, timestamp=timezone.now())

            # Redirect to the list page or some confirmation page
            return HttpResponseRedirect('/events/') 
            
def add_timestamp(request, event_id):
    if request.method == "POST":
        # Get the event by ID
        event = Event.objects.get(id=event_id)
        
        # Create a new EventDetail for this event
        EventDetail.objects.create(event=event, timestamp=timezone.now())

        # Redirect back to the same page
        return HttpResponseRedirect('/events/')
    else:
        # Handle the case where the method is not POST
        return HttpResponseRedirect('/events/')


