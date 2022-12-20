from django.urls import path, include

from . import views

app_name = "about"
urlpatterns = [
    path("", views.about, name="about"),
]
