from django.urls import path
from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name="index"),
    path('add_event', views.add_event, name='add_event'),
    path('add_timestamp/<int:event_id>/', views.add_timestamp, name='add_timestamp'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
