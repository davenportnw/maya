from django.urls import path

from . import views
app_name = 'events'  # This is important for namespacing
urlpatterns = [
    path('', views.index, name="index"),
    path('add_event', views.add_event, name='add_event'),
    path('add_timestamp/<int:event_id>/', views.add_timestamp, name='add_timestamp'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
]   
