from django.http import HttpResponse
from django.shortcuts import render
from .models import Profile

import pandas as pd
from portfolio.functions.funcs import get_covar
import json
import pandas
import portfolio.functions.hello as hello


def portfolio(request):
    return render(request, "port.html")


def create(request):
    if request.method == "POST":
        df = get_covar(json.loads(open("tickers.json").read())["tickers"])
        mydict = {
            "df": df.to_html(
                float_format=lambda x: "%10.2f" % x,
                border=3,
                classes="table table-striped text-center",
                justify="center",
                col_space="38.25px",
            )
        }
        df = df.to_html(
            float_format=lambda x: "%10.2f" % x,
            border=3,
            classes="table table-striped text-center",
            justify="center",
            col_space="38.25px",
        )
        # name = request.POST["name"]
        # if name == "":
        # name = "0"
        # else:
        # pass
        # name = int(name) + 1
        # new_x = Profile(x=x)
        # new_x.save()
        # name = str(name)
        # success = str(name)
        return HttpResponse(df)
