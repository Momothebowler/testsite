import requests
import pandas as pd
import numpy as np
import re
import requests
from lxml import html, etree
import datetime
from .funcs import get_data
import time


def evaulate(request):
    posted_tickers = []
    posted_allocations = []
    posted_send_data = (
        {}
    )  # Data we send to portfoliooptimizer.com (I think is the site)
    recommended_send_data = {}

    recommended_tickers = ["QQQ", "TQQQ"]
    recommended_tickers_allocations = [50, 50]

    # Sets Up posted_Tickers and posted_allocations
    for x in range(int(request.POST["count1"])):
        if request.POST["symbol" + str(x + 1)] != "":
            posted_tickers.append(request.POST["symbol" + str(x + 1)].upper())
            posted_allocations.append(
                int(request.POST["Allocation" + str(x + 1) + "_1"])
            )
    # Computes posted_allocations
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

    # For posted
    for x in range(len(posted_tickers)):
        posted_send_data["symbol" + str(x + 1)] = posted_tickers[x]
        posted_send_data["allocation" + str(x + 1) + "_1"] = posted_allocations[x]

    # selects month-month time period (2) vs year to year (4) DO NOT CHANGE
    posted_send_data["timePeriod"] = 2

    # For recommended
    for x in range(len(posted_tickers)):
        recommended_send_data["symbol" + str(x + 1)] = posted_tickers[x]
        recommended_send_data["allocation" + str(x + 1) + "_1"] = posted_allocations[x]

    # selects month-month time period (2) vs year to year (4) DO NOT CHANGE
    recommended_send_data["timePeriod"] = 2

    frame1 = godDaveMePLease(
        int(request.POST["iters"]),
        INITIAL_ALLOCATIONS,
        posted_tickers,
        posted_send_data,
    )
    time.sleep(5)
    frame2 = godDaveMePLease(
        int(request.POST["iters"]),
        recommended_tickers_allocations,
        recommended_tickers,
        recommended_send_data,
    )

    return frame1, frame2


def godDaveMePLease(loops, allocations, tickers, send_data):
    received_data_dict = {}  # Data we get as we gather
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

    current_loop = 0
    while current_loop <= loops and max_allowed_loops > 0:
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

        #
        # These should be a 1 time run, but aren't?
        #
        try:
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
        except:
            print("I give up")

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
            tickers,
            received_data_dict,
            all_time_dict,
        )
        all_time_dict = _updated_time_dict
        if _continue:
            earliest_year = _earliestYear
            earliest_month = _earliestMonth
            current_loop -= 1
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
        received_data_dict[ticker]
        max_sharpe_percents.append(received_data_dict[ticker])

    # makes our dataframe and passes it back to the ajax request
    returned_portfolio_table = pd.DataFrame(tickers, columns=["Tickers"])
    returned_portfolio_table["Provided"] = allocations
    returned_portfolio_table["Maximum Sharpe"] = max_sharpe_percents
    provided_porfolio = []
    sharpe_portfolio = []
    tot_data_sets = int(len(summary_data) / 24)
    for x in range(12):
        prov_port_summary_sums = 0
        sharpe_port_summary_sums = 0
        for y in range(tot_data_sets):
            # try:
            summary_data[(x * 2) + y * 24] = summary_data[(x * 2) + y * 24].replace(
                ",", ""
            )
            summary_data[(x * 2) + 1 + y * 24] = summary_data[
                ((x * 2) + 1) + y * 24
            ].replace(",", "")
            summary_data[(x * 2) + y * 24] = float(
                re.sub(r"(?!<\d)\.(?!\d)|[^\s\w.]", "", summary_data[(x * 2) + y * 24])
            )
            try:
                summary_data[((x * 2) + 1) + y * 24] = float(
                    re.sub(
                        r"(?!<\d)\.(?!\d)|[^\s\w.]",
                        "",
                        summary_data[((x * 2) + 1) + y * 24],
                    )
                )
            except:
                # print(summary_data)
                print("I'm over here")
            try:
                prov_port_summary_sums += int(summary_data[(x * 2) + y * 24])
                sharpe_port_summary_sums += int(summary_data[((x * 2) + 1) + y * 24])
            except:
                # Skips of N/A
                pass
        # except Exception as e:
        #    print(e)
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

    frame = {"df": returned_portfolio_table, "df2": returned_summary_table}
    return frame
