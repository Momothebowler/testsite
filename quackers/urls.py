from django.urls import path, include

from . import views

app_name = "quackers"
urlpatterns = [
    path("", views.quack, name="quackers"),
]
