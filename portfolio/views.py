from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# import pandas as pd
from portfolio.functions.funcs import get_covar
import json
import pandas
import portfolio.functions.hello as hello


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


def request_page(request):
    #
    # Working on a clicker
    #
    x = 0
    args = {}
    args["x"] = {x}
    try:
        value = request.GET.get("mybtn").strip("{}")
        if request.GET.get("mybtn").strip("{}") == value:
            x = 1 + int(value)
            args["x"] = {x}
        else:
            x = 0
            args["x"] = {x}
        # mydict = {}

        # if mydict != {}:
        #    df = get_covar(json.loads(open("tickers.json").read())["tickers"])
        # df = get_correlation(tickers)
        #    mydict = {
        #        "df": df.to_html(
        #            float_format=lambda x: "%10.2f" % x,
        #            border=3,
        #            classes="table table-striped text-center",
        #            justify="center",
        #            col_space="38.25px",
        #        )
        #    }
    except:
        pass
    return render(request, "port.html", context=args)  # , context=mydict)
