from django.urls import path

from cmb_calendar import views

urlpatterns = [
    path("<int:year>", views.calendar, name="calendar"),
    path("", views.calendar_redirect, name="calendar-redirect"),
]
