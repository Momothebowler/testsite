from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# import pandas as pd
from portfolio.functions.funcs import get_correlation
import json


def portfolio(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # item = money.objects.all().values()

    df = get_correlation(json.loads(open("tickers.json").read())["tickers"])
    # df = get_correlation(tickers)
    mydict = {
        "df": df.to_html(
            border=10, classes="table table-striped text-center", justify="center"
        )
    }
    return render(request, "port.html", context=mydict)
