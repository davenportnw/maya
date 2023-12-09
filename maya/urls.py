from django.contrib import admin
from django.urls import include, path

import events.views

urlpatterns = [
    path('/', events.views.index, name="home"),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls'))
]
