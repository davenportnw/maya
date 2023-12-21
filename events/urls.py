from django.urls import path
# from django.contrib.auth.views import LoginView
# from . import views
# app_name = 'events'  # This is important for namespacing
# urlpatterns = [
#     path('', views.index, name="index"),
#     path('add_event', views.add_event, name='add_event'),
#     path('add_timestamp/<int:event_id>/', views.add_timestamp, name='add_timestamp'),
#     path('edit_occurrence/<int:occurrence_id>/', views.edit_occurrence, name='edit_occurrence'),
#     path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
#     path('register/', views.register, name='register'),
#     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
# ]   

from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name="index"),
    path('add_event', views.add_event, name='add_event'),
    path('add_timestamp/<int:event_id>/', views.add_timestamp, name='add_timestamp'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
