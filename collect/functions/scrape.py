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
from .funcs import get_data


def evaulate(request):
    posted_tickers = []
    posted_allocations = []
    received_data_dict = {}
    send_data = {}
    errors = 0

    #  Gets the tickers and allocations from webpage
    for x in range(int(request.POST["count1"])):
        if request.POST["symbol" + str(x + 1)] != "":
            posted_tickers.append(request.POST["symbol" + str(x + 1)].upper())
            posted_allocations.append(
                int(request.POST["Allocation" + str(x + 1) + "_1"])
            )

    if sum(posted_allocations) != 100:
        posted_allocations = np.full(
            shape=len(posted_tickers),
            fill_value="{:.2f}".format(100 / len(posted_tickers)),
            dtype=np.single,
        )
    sum_allocation = np.sum(posted_allocations)
    if sum_allocation > 100:
        posted_allocations[0] = round(posted_allocations[0] - (sum_allocation - 100), 2)
        posted_allocations = ["".join(item) for item in posted_allocations.astype(str)]
    elif sum_allocation < 100:
        posted_allocations[0] = round(posted_allocations[0] + (100 - sum_allocation), 2)
        posted_allocations = ["".join(item) for item in posted_allocations.astype(str)]

    INITIAL_ALLOCATIONS = posted_allocations

    for x in range(len(posted_tickers)):
        send_data["symbol" + str(x + 1)] = posted_tickers[x]
        send_data["allocation" + str(x + 1) + "_1"] = posted_allocations[x]

    # selects month-month time period (2) vs year to year (4) DO NOT CHANGE
    send_data["timePeriod"] = 2

    today = datetime.date.today()
    CURRENT_YEAR = int(today.year)
    place_holder_year = 1985
    earliest_year = 1985
    earliest_month = 1
    place_holder_month = 1

    all_time_dict = {}
    for n in range(2023 - 1985):
        all_time_dict[str(1985 + n)] = np.arange(1, 13)

    summary_data = []
    max_allowed_loops = 100000

    requested_loops = int(request.POST["iters"])

    current_loop = 0
    while current_loop <= requested_loops and max_allowed_loops > 0:
        max_allowed_loops = len(
            [
                item
                for sublist in (
                    all_time_dict[current_loop] for current_loop in all_time_dict.keys()
                )
                for item in sublist
            ]
        )
        current_loop += 1

        if earliest_year != place_holder_year:
            for x in range(earliest_year - place_holder_year):
                del all_time_dict[str(place_holder_year + x)]
            place_holder_year = earliest_year
        # del all_time_dict["2023"]
        if earliest_month != place_holder_month:
            for x in range(earliest_month - place_holder_month):
                all_time_dict[str(earliest_year)] = np.delete(
                    all_time_dict[str(earliest_year)], x
                )
            place_holder_month = earliest_month

        # try:
        (
            _continue,
            _values,
            _received_data_dict,
            _earliestYear,
            _earliestMonth,
            _updated_time_dict,
        ) = get_data(
            CURRENT_YEAR,
            send_data,
            earliest_month,
            earliest_year,
            posted_tickers,
            received_data_dict,
            all_time_dict,
        )
        all_time_dict = _updated_time_dict
        if _continue:
            earliest_year = _earliestYear
            earliest_month = _earliestMonth
            current_loop -= 1
            errors += 1
            continue
        if _received_data_dict == None:
            continue
        received_data_dict = {**received_data_dict, **_received_data_dict}
        summary_data = summary_data + _values

    # averages the allocations for all tickers individually
    tickers = []
    max_sharpe_percents = []
    for ticker in received_data_dict.keys():
        posted_allocations = received_data_dict[ticker]
        arr2 = []

        for allo in posted_allocations:
            if isinstance(allo, float) or isinstance(allo, int):
                arr2.append(allo)
            else:
                arr2.append(float(allo.replace("%", "")))
        received_data_dict[ticker] = sum(arr2) / len(arr2)
        tickers.append(ticker)
        max_sharpe_percents.append(received_data_dict[ticker])

    # makes our dataframe and passes it back to the ajax request
    returned_portfolio_table = pd.DataFrame(tickers, columns=["Tickers"])
    returned_portfolio_table["Provided"] = INITIAL_ALLOCATIONS
    returned_portfolio_table["Maximum Sharpe"] = max_sharpe_percents

    provided_porfolio = []
    sharpe_portfolio = []
    tot_data_sets = int(len(summary_data) / 24)
    for x in range(12):
        prov_port_summary_sums = 0
        sharpe_port_summary_sums = 0
        for y in range(tot_data_sets):
            try:
                summary_data[(x * 2) + y * 24] = summary_data[(x * 2) + y * 24].replace(
                    ",", ""
                )
            except:
                pass
            try:
                summary_data[(x * 2) + 1 + y * 24] = summary_data[
                    ((x * 2) + 1) + y * 24
                ].replace(",", "")
            except:
                pass
            try:
                summary_data[(x * 2) + y * 24] = float(
                    re.sub(
                        r"(?!<\d)\.(?!\d)|[^\s\w.]", "", summary_data[(x * 2) + y * 24]
                    )
                )
            except:
                pass
            try:
                summary_data[((x * 2) + 1) + y * 24] = float(
                    re.sub(
                        r"(?!<\d)\.(?!\d)|[^\s\w.]",
                        "",
                        summary_data[((x * 2) + 1) + y * 24],
                    )
                )
            except:
                pass
            try:
                prov_port_summary_sums += summary_data[(x * 2) + y * 24]
                sharpe_port_summary_sums += summary_data[((x * 2) + 1) + y * 24]
            except:
                pass
        prov_port_summary_sums = prov_port_summary_sums / tot_data_sets
        sharpe_port_summary_sums = sharpe_port_summary_sums / tot_data_sets
        provided_porfolio.append(round(prov_port_summary_sums, 2))
        sharpe_portfolio.append(round(sharpe_port_summary_sums, 2))
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
    returned_summary_dict = {
        "": col_names,
        "Provided": provided_porfolio,
        "Max Sharpe": sharpe_portfolio,
    }
    returned_summary_table = pd.DataFrame(returned_summary_dict)

    return returned_portfolio_table, returned_summary_table
