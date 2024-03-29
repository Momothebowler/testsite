"""testsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Figure out how to redirect instead of needing both lines
    path("portfolio/", include("portfolio.urls")),
    path("port/", include("portfolio.urls")),
    #
    path("", include("home.urls")),
    path("home/", include("home.urls")),
    #
    path("about/", include("about.urls")),
    path("collect/", include("collect.urls")),
    #
    path("quackers/", include("quackers.urls")),
]
