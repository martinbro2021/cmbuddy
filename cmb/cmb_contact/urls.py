from django.urls import path

from cmb_contact import views

urlpatterns = [
    path("", views.contact),
    path("success/<str:timestamp_str>", views.success, name="send-success")
]
