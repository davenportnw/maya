from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Occurrence
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime
from django.views import generic
from .forms import EventForm

def index(request):
    events = Event.objects.prefetch_related('occurrence_set').all()
    return render(request, "base.html", {'events': events})

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
            Occurrence.objects.create(event=event, timestamp=timezone.now())

            # Redirect to the list page or some confirmation page
            return HttpResponseRedirect('/events/') 
            
def add_timestamp(request, event_id):
    if request.method == "POST":
        # Get the event by ID
        event = Event.objects.get(id=event_id)
        
        # Create a new EventDetail for this event
        Occurrence.objects.create(event=event, timestamp=timezone.now())

        # Redirect back to the same page
        return HttpResponseRedirect('/events/')
    else:
        # Handle the case where the method is not POST
        return HttpResponseRedirect('/events/')

# def edit_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
    # return render(request, 'edit_event.html', {'event': event})

# def update_timestamp(request, detail_id):
#     detail = get_object_or_404(EventDetail, id=detail_id)
#     if request.method == 'POST':
#         timestamp_str = request.POST.get('timestamp')
        
#         # Convert string to datetime object
#         try:
#             converted_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
#             detail.timestamp = converted_timestamp
#             detail.save()
#             return redirect('events:edit_event', event_id=detail.event.id)
#         except ValueError:
#             # Handle the error if the date format is incorrect
#             # You might want to add some form of user notification here
#             pass

#     return redirect('events:edit_event', event_id=detail.event.id)


def edit_event(request, event_id, detail_id=None):
    """
    View function for loading AND editing an event
    """
    # Check if the request is a POST request indicating a form submission
    if request.method == 'GET':
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'edit_event.html', {'event': event})

    if request.method == 'POST':
        detail = get_object_or_404(Occurrence, id=detail_id)
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
    


def delete_timestamp(request, detail_id):
    detail = get_object_or_404(Occurrence, id=detail_id)

    if request.method == 'POST':
        event_id = detail.event.id
        detail.delete()
        return redirect('events:edit_event', event_id=event_id)

    # If not POST, redirect back (or to some other page)
    return redirect('events:edit_event', event_id=detail.event.id)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('events:index')

    # If not POST, redirect back (or to some other page)
    return redirect('events:index')
