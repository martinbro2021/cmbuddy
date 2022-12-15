from django.urls import path

from . import views

urlpatterns = [
    path("", views.contact),
    path("success_<timestamp>", views.success, name="send-success")
]
