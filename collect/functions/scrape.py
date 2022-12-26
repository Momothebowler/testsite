import requests
import lxml.html as lh
import pandas as pd
import numpy as np
import re

import requests
from lxml import html, etree
import re
import pandas as pd


def evaulate(request):
    count = int(request.POST["count"])
    ticks = []
    for x in range(count):
        ticks.append(request.POST["symbol" + str(x + 1)])

    arr = np.full(
        shape=len(ticks),
        fill_value="{:.2f}".format(100 / len(ticks)),
        dtype=np.single,
    )
    sum = np.sum(arr)
    if sum > 100:
        arr[0] = round(arr[0] - (sum - 100), 2)
    elif sum < 100:
        arr[0] = round(arr[0] + (100 - sum), 2)
    arr = ["".join(item) for item in arr.astype(str)]
    data = {}
    for x in range(len(ticks)):
        data["symbol" + str(x + 1)] = ticks[x]
        data["allocation" + str(x + 1) + "_1"] = arr[x]
    url = " https://www.portfoliovisualizer.com/optimize-portfolio"
    page = requests.post(
        url,
        data=data,
    )
    tree = html.fromstring(page.content)
    message = ""
    try:
        message = tree.xpath("/html/body/div[1]/div[3]")
        message = etree.tostring(message[0])
        message = re.findall("</b>(.*?)\n", message.decode("utf-8"))
    except:
        pass

    trs = tree.xpath("/html/body/div[1]/div[6]/div[1]/div[2]/div[2]/div/div[1]/table")
    e = etree.tostring(trs[0])

    ticker = re.findall("<td>(.*?)</td>", str(e))
    percent = re.findall('<td class="numberCell">(.*?)</td>', str(e))

    tickers = []
    for i in range(len(ticker)):
        if i % 2 == 0:
            tickers.append(ticker[i])

    df = pd.DataFrame(tickers, columns=["Tickers"])
    df["Percents"] = percent
    return df, message
