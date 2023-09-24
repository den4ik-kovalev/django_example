from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('', index),
    path('events/', events),
    path('events/<int:event_id>/', event),
    path('events/<int:event_id>/participate/', participate_event),
    path('events/<int:event_id>/exit/', exit_event),
    path('users/<int:user_id>/', user)
]