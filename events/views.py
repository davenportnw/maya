from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventDetail
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime

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

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'edit_event/edit_event.html', {'event': event})

def update_timestamp(request, detail_id):
    detail = get_object_or_404(EventDetail, id=detail_id)

    if request.method == 'POST':
        timestamp_str = request.POST.get('timestamp')
        
        # Convert string to datetime object
        try:
            converted_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
            detail.timestamp = converted_timestamp
            detail.save()
            return redirect('events:edit_event', event_id=detail.event.id)
        except ValueError:
            # Handle the error if the date format is incorrect
            # You might want to add some form of user notification here
            pass

    return redirect('events:edit_event', event_id=detail.event.id)