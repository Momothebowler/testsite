from django.urls import path, include

from . import views

app_name = "portfolio"
urlpatterns = [
    # path("", views.portfolio, name="portfolio"),
    path("", views.request_page, name="portfolio"),
]
