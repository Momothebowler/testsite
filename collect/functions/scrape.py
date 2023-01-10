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

    x = 1
    while x <= 20:

        x += 1
        startYear = random.randint(earliestYear, year - 1)
        endYear = random.randint(startYear + 1, year)
        data["startYear"] = startYear
        data["endYear"] = endYear

        if startYear == earliestYear:
            randMon1 = random.randint(earliestMonth, 12)
        else:
            randMon1 = random.randint(1, 12)
            randMon2 = random.randint(randMon1, 12)

        data["firstMonth"] = randMon1
        data["lastMonth"] = randMon2

        # gets webpage after post request
        url = " https://www.portfoliovisualizer.com/optimize-portfolio"
        page = requests.post(
            url,
            data=data,
        )

        tree = html.fromstring(page.content)
        message = ""

        # gets any update message (might need a sooner time period)
        try:
            message = tree.xpath("/html/body/div[1]/div[3]")
            message = etree.tostring(message[0])
            message3 = None
            try:
                message3 = re.findall(
                    "<div class='alert alert-danger''>(.*?)</div>",
                    message.decode("utf-8"),
                )
            except:
                pass
            if message3 == None or message3 == []:
                message = re.findall("</b>(.*?)\n", message.decode("utf-8"))
            else:
                x -= 1
                continue
            if message != []:
                message2 = re.findall("\[(.*?) -", message[0])[0].split(" ")
                earliestYear = int(message2[1])
                earliestMonth = int(datetime.datetime.strptime(message2[0], "%b").month)
        except Exception as e:
            print(e)
            print(data)
            x -= 1
            continue

        # gets the maximum sharpe ratio table
        trs = tree.xpath("//*[@id='growthChart']/div[2]/div[2]/div/div[1]/table")

        try:
            # Parses table data into tickers and %'s
            e = etree.tostring(trs[0])

            ticker = re.findall("<td>(.*?)</td>", str(e))
            tickers = []
            for i in range(len(ticker)):
                if i % 2 == 0:
                    tickers.append(ticker[i])
            percent = re.findall('<td class="numberCell">(.*?)</td>', str(e))

            for y in range(len(ticks)):
                # checks if its in the dictionary yet and then if it was on the webpage
                # last part is if we a tick with 0% and another with 100% we need
                # to a 0 into the arr for averaging purposes
                if ticks[y] not in data_dict:
                    # Initial add of each ticker (first time scraped)
                    if ticks[y] not in tickers:

                        data_dict[ticks[y]] = [0]
                    else:
                        data_dict[ticks[y]] = [percent[tickers.index(ticks[y])]]
                else:
                    if ticks[y] not in tickers:
                        art = data_dict[ticks[y]]
                        art.append(0)
                        data_dict[ticks[y]] = art
                    else:
                        art = data_dict[ticks[y]]
                        art.append(percent[tickers.index(ticks[y])])
                        data_dict[ticks[y]] = art
        except Exception as ex:
            errors += 1
            print(ex)
            print("total errors: " + str(errors))
            x -= 1

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
    df["Percents"] = percent
    timePer = (
        str(data["startYear"])
        + "-"
        + str(data["firstMonth"])
        + " - "
        + str(data["endYear"])
        + "-"
        + str(data["lastMonth"])
    )
    df.index.name = 0
    df.columns.name = timePer
    df.index.name = None
    return df
