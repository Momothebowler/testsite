from django.shortcuts import render, HttpResponse

# from collect.functions.scrape import getSpy
from collect.functions.scrape_old import evaulate
import json


def quack(request):
    return render(request, "quack.html")
