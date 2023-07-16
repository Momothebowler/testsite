from django.urls import path, include

from . import views

app_name = "sliders"
urlpatterns = [
    path("", views.sliders, name="sliders"),
]
