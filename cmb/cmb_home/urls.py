from django.urls import path

from cmb_home import views

urlpatterns = [
    path("", views.home_redirect),
    path("home/", views.home, name="home"),
]
