from django.urls import path
from . import views

urlpatterns = [
    path("lookup/<str:code>/", views.lookup_room, name="lookup_room"),
]
