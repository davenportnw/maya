import re

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Occurrence, CollaborationInvitation
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models import Subquery, OuterRef, Q
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse


#  ============= Homepage/Events =============
@login_required
def index(request):    
    subquery = Occurrence.objects.filter(
        event=OuterRef('pk')
    ).order_by('-timestamp')

    events = Event.objects.filter(
        Q(user=request.user) | Q(collaborators=request.user)
    ).annotate(
        timestamp=Subquery(subquery.values('timestamp')[:1])
    ).distinct().order_by('-timestamp')
    

    # Handle the search query
    search_query = request.GET.get('search', '')
    if search_query:
         events = events.filter(Q(name__icontains=search_query))

    # Handle collab events
    # Fetch pending invitations for the current user
    pending_invitations = CollaborationInvitation.objects.filter(
        invitee=request.user, 
        accepted=None 
    )
    return render(request, "home.html", {'events': events, 'search_query': search_query, 'pending_invitations': pending_invitations})


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
            return HttpResponseRedirect('/') 
        else:
            # Add a message for empty event name
            messages.error(request, 'Please write an event name.')

        return HttpResponseRedirect('/')
     
@login_required
def add_timestamp(request, event_id):
    if request.method == "POST":
        # Get the event by ID
        event = Event.objects.get(id=event_id)
        
        # Create a new EventDetail for this event
        Occurrence.objects.create(event=event, timestamp=timezone.now())

        # Redirect back to the same page
        return HttpResponseRedirect('/')
    else:
        # Handle the case where the method is not POST
        return HttpResponseRedirect('/')


@login_required
def edit_occurrence(request, occurrence_id=None):
    occurrence = get_object_or_404(Occurrence, id=occurrence_id)
    event = occurrence.event
    if request.method == 'POST':
        # Check if this is a delete action
        if request.POST.get('action') == 'delete':
            occurrence.delete()
            messages.success(request, 'Occurrence deleted successfully.')
            return redirect('index')

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
            return redirect('index')

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
            return redirect('index')

    invitations = CollaborationInvitation.objects.filter(event=event, accepted=None) 
    invited_users_with_invitations = [
        {'user': invitation.invitee, 'invitation_id': invitation.id} for invitation in invitations
    ]
    collaborators = event.collaborators.all() 
    return render(request, 'edit_event.html', {'event': event, 'invited_users_with_invitations': invited_users_with_invitations, 'collaborators': collaborators } )


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.user:
        if request.method == 'POST':
            event.delete()
            messages.success(request, 'Deletion successful.')
            return redirect('index')
    else:
        messages.error(request, "You do not have permission to delete this event.")
    return redirect('edit_event', event_id=event_id)


#  ============= Login/Registration  =============
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login') 
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
                return redirect('index')  # Redirect to a home page or dashboard
        else:
            # Handle field-specific errors
            for field_name in form.errors:
                for error in form.errors[field_name]:
                    messages.error(request, error)

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')    


#  ============= Collaborated Events =============
def send_invitation(request, event_id):
    invitee_username = request.POST.get('invitee_username')
    event = get_object_or_404(Event, id=event_id)
    sender = request.user
    if request.method == 'POST':
        try:
            invitee = User.objects.get(username=invitee_username) 
            # Prevent sending an invitation to oneself
            if sender == invitee:
                messages.error(request, "You cannot send an invitation to yourself.")
                print("can't send invite to yourself bro")
                return redirect('edit_event', event_id=event_id)
            # Check if an invitation already exists
            elif CollaborationInvitation.objects.filter(event=event, sender=sender, invitee=invitee).exists():
                messages.error(request, "An invitation has already been sent to this user.")
                return redirect('edit_event', event_id=event_id)
            else:
            # Create and save the invitation
                CollaborationInvitation.objects.create(
                    event=event,
                    sender=sender,
                    invitee=invitee,
                    accepted=None  # or leave this out if None is the default
                )
                messages.success(request,'Invite Sent!')
            # Redirect to a confirmation page, or handle as needed
        except User.DoesNotExist:
            messages.error(request, 'Invalid Username')
        return redirect('edit_event', event_id=event_id)
    return redirect('edit_event', event_id=event_id)

def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(CollaborationInvitation, id=invitation_id, invitee=request.user, accepted=None)
    if invitation.accepted is not True:
        invitation.accepted = True
        invitation.save()
        messages.success(request, 'You have accepted the invitation.')
        invitation.event.collaborators.add(request.user)
    else:
        messages.info(request, "You have already accepted this invitation")
    return redirect('index')

def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(CollaborationInvitation, id=invitation_id, invitee=request.user)
    invitation.accepted = False
    invitation.save()
    messages.success(request, "You have declined the invitation.")
    return redirect('index')  

def cancel_invitation(request, invitation_id):
    invitation = get_object_or_404(CollaborationInvitation, pk=invitation_id)
    print('before') 
    # Ensure the request is made by the event owner or the one who sent the invite
    if request.user == invitation.event.user:
        invitation.delete()  # Or mark as canceled if you have a status field
        messages.success(request, "Invitation canceled successfully.")
    else:
        messages.error(request, "You don't have permission to cancel this invitation.")
    return HttpResponseRedirect(reverse('edit_event', args=[invitation.event.id]))

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the current user is not the owner of the event
    if request.user != event.user:
        # Check if the current user is a collaborator
        if request.user in event.collaborators.all():
            event.collaborators.remove(request.user)
            event.save()
            messages.success(request, "You have left the event successfully.")
        else:
            messages.info(request, "You are not a collaborator of this event.")
    else:
        messages.error(request, "As the owner, you cannot leave the event. You may delete it instead.")

    return redirect('index') 