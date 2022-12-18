# from django.urls import url
#
# from . import views
#
# app_name = "polls"
# urlpatterns = [
#    url(r"^$", views.IndexView.as_view(), name="index"),
#    url(r"^(?P<pk>\d+)/$", views.DetailView.as_view(), name="detail"),
#    ...,
# ]

from django.urls import path, include

from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
]
