from django.urls import path

from monitoring import views

urlpatterns = [
    path("url/", views.urls_view,name = "urls"),
    path("url/heartbeat/", views.get_heartbeat_view, name="heartbeat"),
    path("alerts/", views.get_alerts_view, name="alerts"),
]