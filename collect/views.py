from django.shortcuts import render, HttpResponse

# from collect.functions.scrape import getSpy
from collect.functions.scrape import spyGet, evaulate


def collect(request):
    return render(request, "collect.html")


def create(request):
    if request.method == "POST":
        tickers = ["TSLA", "AMZN", "AAPL", "GOOG", "NOK", "BBBY", "GME"]
        df = evaulate(tickers)
        mydict = {
            "df": df.to_html(
                float_format=lambda x: "%10.2f" % x,
                border=3,
                classes="table table-striped text-center",
                justify="center",
                col_space="38.25px",
            )
        }
        df.index += 1
        df = df.to_html(
            float_format=lambda x: "%10.2f" % x,
            border=3,
            classes="table table-striped text-center",
            justify="center",
            col_space="38.25px",
        )
        return HttpResponse(df)
