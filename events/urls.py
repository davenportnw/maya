from django.urls import path

from . import views
app_name = 'events'  # This is important for namespacing
urlpatterns = [
    path('', views.index, name="index"),
]