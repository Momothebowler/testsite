from django.shortcuts import render, HttpResponse

# from collect.functions.scrape import getSpy
from collect.functions.scrape import evaulate
import json
import pandas as pd


def collect(request):
    return render(request, "collect.html")


def create(request):
    if request.method == "POST":
        frame, frame2 = evaulate(request)  # tickers)

        frame["df2"] = frame["df2"].rename(
            columns={"": "Tickers", "Max Sharpe": "Maximum Sharpe"}
        )
        df = pd.concat(
            [frame["df"], frame["df2"]],
            ignore_index=True,
        )

        df2 = df.to_html(
            float_format=lambda x: "%10.2f" % x,
            # border=3,
            # classes="table table-striped text-center table-hover",
            justify="center",
            # col_space="38.25px",
            index=False,
        )
        frame2["df2"] = frame["df2"].rename(
            columns={"": "Tickers", "Max Sharpe": "Maximum Sharpe"}
        )
        df3 = pd.concat(
            [frame2["df"], frame2["df2"]],
            ignore_index=True,
        )

        df4 = df3.to_html(
            float_format=lambda x: "%10.2f" % x,
            # border=3,
            # classes="table table-striped text-center table-hover",
            justify="center",
            # col_space="38.25px",
            index=False,
        )
        data = {"df": df2, "df2": df4}
        return HttpResponse(json.dumps(data))
