from django.http import HttpResponse
from django.shortcuts import render

from portfolio.functions.funcs import get_covar
import json


def portfolio(request):
    return render(request, "port.html")
