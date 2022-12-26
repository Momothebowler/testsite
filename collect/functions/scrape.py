import requests
import lxml.html as lh
import pandas as pd
import numpy as np
import re

import requests
from lxml import html, etree
import re
import pandas as pd


def evaulate():
    tickers = [
        "TSLA",
        "AMZN",
        "AAPL",
        "GOOG",
        "NOK",
        "BBBY",
        "GME",
        "QQQ",
        "TQQQ",
        "AMC",
        "BB",
    ]
    ticks = tickers
    arr = np.full(
        shape=len(ticks), fill_value=round((100 / len(ticks)), 2), dtype=np.float16
    )
    total = round(round((100 / len(ticks)), 2) * len(ticks), 2)
    if total < 100:
        arr[0] += round(100 - total, 2)
    elif total > 100:
        arr[0] = round(arr[0] - (total - 100), 2)
    arr = ["".join(item) for item in arr.astype(str)]

    data = {}
    for x in range(len(tickers)):
        data["symbol" + str(x + 1)] = tickers[x]
        data["allocation" + str(x + 1) + "_1"] = arr[x]
    url = " https://www.portfoliovisualizer.com/optimize-portfolio"
    page = requests.post(
        url,
        data=data,
    )
    tree = html.fromstring(page.content)
    trs = tree.xpath(
        "/html/body/div[1]/div[6]/div[1]/div[2]/div[2]/div/div[1]/table/tbody"
    )
    e = etree.tostring(trs[0], pretty_print=True)

    ticker = re.findall("<td>(.*?)</td>", str(e))
    percent = re.findall('<td class="numberCell">(.*?)</td>', str(e))

    tickers = []
    for i in range(len(ticker)):
        if i % 2 == 0:
            tickers.append(ticker[i])

    df = pd.DataFrame(tickers, columns=["Tickers"])
    df["Percents"] = percent
    return df
