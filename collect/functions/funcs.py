import requests
from lxml import html, etree
import datetime
import re
import numpy as np
import random


def get_data(
    year,
    data2,
    earliestMonth,
    earliestYear,
    ticks,
    data_dict2,
    time_dict,
):
    values = []
    data_dict = {}
    data = data2
    # Considers that it's 2023 and only 1 month has passed

    time_dict1 = time_dict

    startYear = random.choice(list(time_dict1))
    if startYear != year:
        data["startYear"] = startYear
        data["endYear"] = str(int(startYear) + 1)
    else:
        data["endYear"] = startYear
        data["startYear"] = str(int(startYear) - 1)

    try:
        data["firstMonth"] = np.random.choice(time_dict1[data["startYear"]], size=1)[0]
    except:
        del time_dict1[data["startYear"]]
        return True, [], {}, earliestYear, earliestMonth, time_dict1
    data["lastMonth"] = data["firstMonth"]

    time_dict1[str(data["startYear"])] = np.delete(
        time_dict1[str(data["startYear"])],
        np.where(time_dict1[str(data["startYear"])] == data["firstMonth"]),
    )

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
    except:
        pass

    # Checks for the big bad error first
    try:
        message4 = tree.xpath("/html/body/div[1]/div[2]")  # looks for an error message
        message4 = etree.tostring(message4[0])
        message5 = re.findall(
            "is (.*?)<br/>",
            message4.decode("utf-8"),
        )
        if message5 != []:
            message5 = message5[0].split(" - ")[0].split(" ")
            earliestYear = int(message5[1])
            earliestMonth = int(datetime.datetime.strptime(message5[0], "%b").month)
            return True, [], {}, earliestYear, earliestMonth, time_dict1
    except Exception as e:
        print(e)
        pass

    try:
        message3 = tree.xpath("/html/body/div[1]/div[3]")  # looks for an error message
        message3 = re.findall(
            "<div class='alert alert-danger''>(.*?)</div>",
            message.decode("utf-8"),
        )
        if message3 != []:
            message3 = re.findall("</b>(.*?)\n", message.decode("utf-8"))
            message3 = re.findall("\[(.*?) -", message[0])[0].split(" ")
            earliestYear = int(message3[1]) + 1
            earliestMonth = int(datetime.datetime.strptime(message3[0], "%b").month)
            return True, [], {}, earliestYear, earliestMonth, time_dict1
    except Exception as e:
        pass

    # gets the maximum sharpe ratio table
    trs = tree.xpath("//*[@id='growthChart']/div[2]/div[2]/div/div[1]/table")
    trss = tree.xpath("//*[@id='growthChart']/div[3]")

    try:
        # Parses table data into tickers and %'s
        e = etree.tostring(trs[0])
        s = etree.tostring(trss[0])

        value = re.findall('<td class="numberCell">(.*?)</td>', str(s))

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
            if ticks[y] not in data_dict2:
                # Initial add of each ticker (first time scraped)
                if ticks[y] not in tickers:

                    data_dict[ticks[y]] = [0]
                else:
                    data_dict[ticks[y]] = [percent[tickers.index(ticks[y])]]
            else:
                if ticks[y] not in tickers:
                    art = data_dict2[ticks[y]]
                    art.append(0)
                    data_dict[ticks[y]] = art
                else:
                    art = data_dict2[ticks[y]]
                    art.append(percent[tickers.index(ticks[y])])
                    data_dict[ticks[y]] = art
        for pp in value:
            try:
                ppp = pp.split("/> ")
                values.append(ppp[1])
            except:
                values.append(pp)
    except Exception as ex:
        print(ex)
        print(data)
        return True, [], {}, earliestYear, earliestMonth, time_dict1
    return False, values, data_dict, earliestYear, earliestMonth, time_dict1
