#
# Goes to portfoliooptimizer.com/optimize
# plugs in tickers entered in on webpage and allocations
# sends a post request
# returns the percentages from the maximum sharpe ratio table
# repeats 20 times and averages
# sends a dataframe with the averages
#


import requests
import pandas as pd
import numpy as np
import re
import requests
from lxml import html, etree
import datetime
import random
from .funcs import get_data


def evaulate(request):
    ticks = []  # Tickers from Post
    arr = []  # Allocations from Post
    data_dict = {}
    data = {}
    errors = 0

    #  Gets the tickers and allocations from webpage
    for q in range(int(request.POST["count1"])):
        if request.POST["symbol" + str(q + 1)] != "":
            ticks.append(request.POST["symbol" + str(q + 1)].upper())
            arr.append(int(request.POST["Allocation" + str(q + 1) + "_1"]))
    # if typed allocations dont sum to 100%, sets all of them to about equal
    if sum(arr) != 100:
        arr = np.full(
            shape=len(ticks),
            fill_value="{:.2f}".format(100 / len(ticks)),
            dtype=np.single,
        )
    sums = np.sum(arr)
    if sums > 100:
        arr[0] = round(arr[0] - (sums - 100), 2)
        arr = ["".join(item) for item in arr.astype(str)]
    elif sums < 100:
        arr[0] = round(arr[0] + (100 - sums), 2)
        arr = ["".join(item) for item in arr.astype(str)]

    arty = []
    arty = arty + arr
    # puts the tickers and allocations into a data dict to pass into a post request
    for r in range(len(ticks)):
        data["symbol" + str(r + 1)] = ticks[r]
        data["allocation" + str(r + 1) + "_1"] = arr[r]

    # selects month-month time period vs year to year (4)
    data["timePeriod"] = 2

    today = datetime.date.today()
    year = int(today.year)
    earliestYear = 1985
    earliestMonth = 1

    values = []
    x = 1
    while x <= int(request.POST["iters"]):

        x += 1

        startYear = random.randint(earliestYear, year)
        data["startYear"] = startYear
        # % is modulo

        if startYear == earliestYear:
            randMon1 = random.randint(earliestMonth, 12)
        else:
            randMon1 = random.randint(1, 12)
        # 1 year difference (fixed)

        endYear = startYear + 1

        # Considers that it's 2023 and only 1 month has passed
        if endYear == year:
            randMon1 = 1
        if endYear == year + 1:
            endYear -= 1
            startYear -= 1

        # try:
        cont, _values, _data_dict, _earliestYear, _earliestMonth = get_data(
            year,
            startYear,
            randMon1,
            data,
            earliestMonth,
            earliestYear,
            ticks,
            data_dict,
        )
        if cont:
            earliestYear = _earliestYear
            earliestMonth = _earliestMonth
            x -= 1
            errors += 1
            continue
        if _data_dict == None:
            continue
        data_dict = {**data_dict, **_data_dict}
        values = values + _values

    # averages the allocations for all tickers individually
    tickers = []
    percent = []
    for x in data_dict.keys():
        arr = data_dict[x]
        arr2 = []

        for p in arr:
            if isinstance(p, float) or isinstance(p, int):
                arr2.append(p)
            else:
                arr2.append(float(p.replace("%", "")))
        data_dict[x] = sum(arr2) / len(arr2)
        tickers.append(x)
        percent.append(data_dict[x])

    # makes our dataframe and passes it back to the ajax request
    df = pd.DataFrame(tickers, columns=["Tickers"])
    df["Provided"] = arty
    df["Maximum Sharpe"] = percent

    provided = []
    sharpe = []
    hehe = int(len(values) / 24)
    for x in range(12):
        sumy = 0
        sumy2 = 0
        for y in range(hehe):
            try:
                values[(x * 2) + y * 24] = values[(x * 2) + y * 24].replace(",", "")
            except:
                pass
            try:
                values[(x * 2) + 1 + y * 24] = values[((x * 2) + 1) + y * 24].replace(
                    ",", ""
                )
            except:
                pass
            try:
                values[(x * 2) + y * 24] = float(
                    re.sub(r"(?!<\d)\.(?!\d)|[^\s\w.]", "", values[(x * 2) + y * 24])
                )
            except:
                pass
            try:
                values[((x * 2) + 1) + y * 24] = float(
                    re.sub(
                        r"(?!<\d)\.(?!\d)|[^\s\w.]", "", values[((x * 2) + 1) + y * 24]
                    )
                )
            except:
                pass
            try:
                sumy += values[(x * 2) + y * 24]
                sumy2 += values[((x * 2) + 1) + y * 24]
            except:
                pass
        sumy = sumy / hehe
        sumy2 = sumy2 / hehe
        provided.append(round(sumy, 2))
        sharpe.append(round(sumy2, 2))
    col_names = [
        "Start Balance",
        "End Balance",
        "Annualized Return",
        "Expected Return",
        "Standard Deviation",
        "Best Year",
        "Worst Year",
        "Max Drawdown",
        "Sharpe Ratio (ex-ante)",
        "Sharpe Ratio (ex-post)",
        "Sortino Ration",
        "Stock Market Correlation",
    ]
    d = {"": col_names, "Provided": provided, "Max Sharpe": sharpe}
    df2 = pd.DataFrame(d)
    return df, df2
