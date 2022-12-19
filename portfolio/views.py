from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# import pandas as pd
from portfolio.functions.funcs import get_covar
import json
import pandas


def portfolio(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # item = money.objects.all().values()

    df = get_covar(json.loads(open("tickers.json").read())["tickers"])
    # df = get_correlation(tickers)
    mydict = {
        "df": df.to_html(
            float_format=lambda x: "%10.2f" % x,
            border=3,
            classes="table table-striped text-center",
            justify="center",
            col_space="38.25px",
        )
    }
    return render(request, "port.html", context=mydict)
