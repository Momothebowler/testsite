import requests
from lxml import html, etree
import datetime
import re
import numpy as np
import random


def get_data(
    CURRENT_YEAR,
    send_data,
    earliest_month,
    earliest_year,
    posted_tickers,
    received_data_dict,
    all_time_dict,
):
    _summary_data = []
    data_dict2 = received_data_dict
    # Considers that it's 2023 and only 1 month has passed

    start_year = random.choice(list(all_time_dict))
    if start_year != CURRENT_YEAR:
        send_data["startYear"] = start_year
        send_data["endYear"] = str(int(start_year) + 1)
    else:
        send_data["endYear"] = start_year
        send_data["startYear"] = str(int(start_year) - 1)

    try:
        send_data["firstMonth"] = np.random.choice(
            all_time_dict[send_data["startYear"]], size=1
        )[0]
    except:
        del all_time_dict[send_data["startYear"]]
        return True, [], {}, earliest_year, earliest_month, all_time_dict
    send_data["lastMonth"] = send_data["firstMonth"]

    all_time_dict[str(send_data["startYear"])] = np.delete(
        all_time_dict[str(send_data["startYear"])],
        np.where(all_time_dict[str(send_data["startYear"])] == send_data["firstMonth"]),
    )

    # gets webpage after post request
    url = " https://www.portfoliovisualizer.com/optimize-portfolio"
    page = requests.post(
        url,
        data=send_data,
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
            earliest_year = int(message5[1])
            earliest_month = int(datetime.datetime.strptime(message5[0], "%b").month)
            return True, [], {}, earliest_year, earliest_month, all_time_dict
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
            earliest_year = int(message3[1]) + 1
            earliest_month = int(datetime.datetime.strptime(message3[0], "%b").month)
            return True, [], {}, earliest_year, earliest_month, all_time_dict
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
        tickers = [ticker[i] for i in range(len(ticker)) if i % 2 == 0]

        percent = re.findall('<td class="numberCell">(.*?)</td>', str(e))

        for y in range(len(posted_tickers)):
            # checks if its in the dictionary yet and then if it was on the webpage
            # last part is if we a tick with 0% and another with 100% we need
            # to a 0 into the arr for averaging purposes
            if posted_tickers[y] not in data_dict2:
                # Initial add of each ticker (first time scraped)
                if posted_tickers[y] not in tickers:

                    received_data_dict[posted_tickers[y]] = [0]
                else:
                    received_data_dict[posted_tickers[y]] = [
                        percent[tickers.index(posted_tickers[y])]
                    ]
            else:
                if posted_tickers[y] not in tickers:
                    art = data_dict2[posted_tickers[y]]
                    art.append(0)
                    received_data_dict[posted_tickers[y]] = art
                else:
                    art = data_dict2[posted_tickers[y]]
                    art.append(percent[tickers.index(posted_tickers[y])])
                    received_data_dict[posted_tickers[y]] = art
        for pp in value:
            try:
                ppp = pp.split("/> ")
                _summary_data.append(ppp[1])
            except:
                _summary_data.append(pp)
    except Exception as ex:
        print(ex)
        print(send_data)
        return True, [], {}, earliest_year, earliest_month, all_time_dict
    return (
        False,
        _summary_data,
        received_data_dict,
        earliest_year,
        earliest_month,
        all_time_dict,
    )
