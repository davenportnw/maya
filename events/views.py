from django.shortcuts import render
from .models import Event, EventDetail
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    events = Event.objects.prefetch_related('eventdetail_set').all()
    return render(request, "landing/base.html", {'events': events})

def add_event(request):
    # if request.method == "POST":
        
    #     # event_name = request.POST.get('event_name')
    #     event_name = request.POST.get('event_name').strip().lower()    
    #     if event_name:
    #         # Check if an Event with this name already exists
    #         event, created = Event.objects.get_or_create(name=event_name)

    #         # Create a new EventDetail for this event
    #         EventDetail.objects.create(event=event, timestamp=timezone.now())
            
    #         # Redirect to the list page or some confirmation page
    #         return HttpResponseRedirect('/events/')  # Adjust the URL as needed
    # # Redirect back to the form page if not a POST request or if the name is empty
    # return HttpResponseRedirect('/events/')
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
   


