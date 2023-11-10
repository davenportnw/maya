from django.shortcuts import render
from .models import Event


# Create your views here.
def index(request):
    events = Event.objects.all()
    return render(request, "landing/base.html",{'events': events})

