from django.shortcuts import render, HttpResponse

# from collect.functions.scrape import getSpy
from collect.functions.scrape import evaulate
import json


def collect(request):
    return render(request, "collect.html")


def create(request):
    if request.method == "POST":
        df, message = evaulate(request)  # tickers)
        # mydict = {
        #    "df": df.to_html(
        #        float_format=lambda x: "%10.2f" % x,
        #        border=3,
        #        classes="table table-striped text-center",
        #        justify="center",
        #        col_space="38.25px",
        #    )
        # }
        df.index += 1
        df = df.to_html(
            float_format=lambda x: "%10.2f" % x,
            border=3,
            classes="table table-striped text-center",
            justify="center",
            col_space="38.25px",
        )
        data = {
            "df": df,
            "message": message,
        }
        return HttpResponse(json.dumps(data))
