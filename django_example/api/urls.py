from django.urls import path, include

from .views import *

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("CreateUser", CreateUserView.as_view()),
    path("CreateEvent/", CreateEventView.as_view()),
    path("GetEventList/", GetEventListView.as_view()),
    path("AddParticipant/", AddParticipantView.as_view()),
    path("RemoveParticipant/", RemoveParticipantView.as_view()),
    path("DeleteEvent/", DeleteEventView.as_view())
]