from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.index, name='index'),
    path('login/', event_views.login_view, name='login'),
    path('logout/', event_views.logout_view, name='logout'),
    path('register/', event_views.register, name='register'),
    path('edit_occurrence/<int:occurrence_id>/', event_views.edit_occurrence, name='edit_occurrence'),
    path('edit_event/<int:event_id>/', event_views.edit_event, name='edit_event'),
    path('events/', include('events.urls'), name='events'),
]
