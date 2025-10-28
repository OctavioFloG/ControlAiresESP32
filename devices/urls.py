from django.urls import path
from . import views

app_name = "devices"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("toggle/<int:pk>/", views.toggle_device, name="toggle"),
    # API para ESP32:
    path("api/heartbeat/", views.api_heartbeat, name="api_heartbeat"),
    path("api/command/", views.api_command, name="api_command"),
]
