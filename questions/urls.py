from django.urls import path, include

from . import views

app_name = "questions"
urlpatterns = [
    path("", views.questions, name="questions"),
]
