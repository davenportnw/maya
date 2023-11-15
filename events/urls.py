from django.urls import path

from . import views
app_name = 'events'  # This is important for namespacing
urlpatterns = [
    path('', views.index, name="index"),
    path('add_event', views.add_event, name='add_event'),

]   
