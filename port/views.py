from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# import pandas as pd
from funcs import get_correlation
import json


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # item = money.objects.all().values()

    df = get_correlation(json.loads(open("tickers.json").read())["tickers"])
    # df = get_correlation(tickers)
    mydict = {"df": df.to_html()}
    return render(request, "index.html", context=mydict)
