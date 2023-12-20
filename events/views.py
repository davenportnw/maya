import re

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Occurrence
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models import Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import logout

@login_required
def index(request):    
    subquery = Occurrence.objects.filter(
        event=OuterRef('pk')
    ).order_by('-timestamp')

    events = Event.objects.filter(
        user=request.user
    ).annotate(
        timestamp=Subquery(subquery.values('timestamp')[:1])
    ).order_by('-timestamp')
    return render(request, "home.html", {'events': events})


@login_required
def add_event(request):
     if request.method == "POST":
        event_name = request.POST.get('event_name').strip()

        if event_name:
            # Try to get an event with a case-insensitive match
            event = Event.objects.filter(name__iexact=event_name, user=request.user).first()

            # If event does not exist, create a new one
            if not event:
                event = Event.objects.create(name=event_name, user=request.user)

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
    event = occurrence.event
    if request.method == 'POST':

        # Check if this is a delete action
        if request.POST.get('action') == 'delete':
            occurrence.delete()
            messages.success(request, 'Occurrence deleted successfully.')
            return redirect('events:index')

        update_needed = False

        # Handle the save action for the timestamp
        timestamp_str = request.POST.get('timestamp')
        if timestamp_str:
            try:
                converted_timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y')
                occurrence.timestamp = converted_timestamp
                update_needed = True
            except ValueError:
                messages.error(request, 'Invalid date format.')

        # Handle the save action for the time of day
        timeofday_str = request.POST.get('timeofday')
        if timeofday_str:
            if re.match(r'^\d{2}:\d{2}$', timeofday_str):
                try:
                    time_of_day = datetime.strptime(timeofday_str, '%H:%M').time()
                    if timestamp_str:
                        occurrence.timeofday = datetime.combine(occurrence.timestamp.date(), time_of_day)
                    else:
                        occurrence.timeofday = datetime.combine(occurrence.timestamp.date(), time_of_day)
                    update_needed = True
                except ValueError:
                    messages.error(request, 'Invalid time format.')
            else:
                messages.error(request, 'Time format does not match HH:MM.')
        # import ipdb; ipdb.set_trace()
    
        # Handle the save action for notes
        note_str = request.POST.get('note')
        if note_str is not None:
            occurrence.note = note_str
            update_needed = True

        if update_needed:
            occurrence.save()
            messages.success(request, 'Update successful.')
            return redirect('events:index')

    return render(request, 'edit_occurrence.html', {'occurrence': occurrence, 'event': event})

@login_required
def edit_event(request, event_id=None):
    event = get_object_or_404(Event, id=event_id)  # Replace 'Event' with your event model

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        if event_name:
            event.name = event_name  # Replace 'name' with your event name field
            event.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('events:index')

    return render(request, 'edit_event.html', {'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Deletion successful.')
        return redirect('events:index')

    # If not POST, redirect back (or to some other page)
    return redirect('events:index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('events:login') 
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
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
                 messages.error(request, 'Invalid username or password.')
        else:
            for error in form.non_field_errors():
                print('Non-field error: ', error)
                messages.error(request, error)

            for field in form.errors:
                for error in form[field].errors:
                    print(f'Field error in {field}: ', error)
                    messages.error(request, error)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('events:index') 