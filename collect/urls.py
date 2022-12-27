from django.urls import path, include

from . import views

app_name = "collect"
urlpatterns = [
    path("", views.collect, name="collect"),
    path("create", views.create, name="create"),
]
