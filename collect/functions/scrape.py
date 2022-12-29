import requests
import lxml.html as lh
import pandas as pd
import numpy as np
import re

import requests
from lxml import html, etree
import re
import pandas as pd

import datetime
import random


def evaulate(request):
    ticks = []
    arr = []
    data_dict = {}
    data = {}
    errors = 0
    for q in range(int(request.POST["count1"])):
        if request.POST["symbol" + str(q + 1)] != "":
            ticks.append(request.POST["symbol" + str(q + 1)].upper())
            arr.append(request.POST["Allocation" + str(q + 1) + "_1"])
        arr = np.full(
            shape=len(ticks),
            fill_value="{:.2f}".format(100 / len(ticks)),
            dtype=np.single,
        )
        sums = np.sum(arr)
        if sums > 100:
            arr[0] = round(arr[0] - (sums - 100), 2)
        elif sums < 100:
            arr[0] = round(arr[0] + (100 - sums), 2)
        arr = ["".join(item) for item in arr.astype(str)]

    for r in range(len(ticks)):
        data["symbol" + str(r + 1)] = ticks[r]
        data["allocation" + str(r + 1) + "_1"] = arr[r]

    data["timePeriod"] = 2

    today = datetime.date.today()
    year = int(today.year)

    x = 1
    while x <= 20:
        print("loop: " + str(x))
        x += 1

        startYear = random.randint(1985, year - 1)
        endYear = random.randint(startYear + 1, year)
        data["startYear"] = startYear
        data["endYear"] = endYear

        randMon1 = random.randint(1, 12 - 1)
        randMon2 = random.randint(randMon1 + 1, 12)

        data["firstMonth"] = randMon1
        data["lastMonth"] = randMon2

        url = " https://www.portfoliovisualizer.com/optimize-portfolio"
        page = requests.post(
            url,
            data=data,
        )
        tree = html.fromstring(page.content)
        message = ""
        message = tree.xpath("/html/body/div[1]/div[3]")
        message = etree.tostring(message[0])
        message = re.findall("</b>(.*?)\n", message.decode("utf-8"))

        trs = tree.xpath("//*[@id='growthChart']/div[2]/div[2]/div/div[1]/table")

        try:
            e = etree.tostring(trs[0])
            ticker = re.findall("<td>(.*?)</td>", str(e))
            tickers = []
            for i in range(len(ticker)):
                if i % 2 == 0:
                    tickers.append(ticker[i])
            percent = re.findall('<td class="numberCell">(.*?)</td>', str(e))

            for y in range(len(ticks)):
                if ticks[y] not in data_dict:
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
    return df, message
