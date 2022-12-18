from django.urls import path

from . import views

urlpatterns = [
    path("", views.contact),
    path("success/<timestamp>", views.success, name="send-success")
]
