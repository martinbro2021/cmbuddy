from django.urls import path

from cmb_contact import views

urlpatterns = [
    path("", views.contact),
    path("success/<timestamp>", views.success, name="send-success")
]
