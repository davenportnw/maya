from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Occurrence
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    events = Event.objects.prefetch_related('occurrence_set').all()
    return render(request, "base.html", {'events': events})
@login_required
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
        else:
            # Add a message for empty event name
            messages.error(request, 'Please write an event name.')

        return HttpResponseRedirect('/events/')
     
@login_required
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
@login_required
def edit_occurrence(request, occurrence_id=None):
    occurrence = get_object_or_404(Occurrence, id=occurrence_id)

    if request.method == 'POST':
        # Check if this is a delete action
        if request.POST.get('action') == 'delete':
            occurrence.delete()
            return redirect('events:index')

        # Handle the save action (updating the timestamp)
        timestamp_str = request.POST.get('timestamp')
        if timestamp_str:
            try:
                converted_timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y')
                occurrence.timestamp = converted_timestamp
                occurrence.save()
            except ValueError:
                # Handle the error if the date format is incorrect
                pass
            return redirect('events:index')
        else:
            # Handle the case where timestamp is None
            pass

    return render(request, 'edit_occurrence.html', {'occurrence': occurrence})
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('events:index')

    # If not POST, redirect back (or to some other page)
    return redirect('events:index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
        print('invalid creation')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('events:index')  # Redirect to a home page or dashboard
            else:
                # Invalid login
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

