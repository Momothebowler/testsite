import requests
from lxml import html, etree
import datetime
import re
import numpy as np
import random
import traceback


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

    # Checks for the big bad error first
    try:
        bad_message = tree.xpath(
            "/html/body/div[1]/div[2]"
        )  # looks for an error message
        bad_message = etree.tostring(bad_message[0]).decode()
        if "alert alert-danger" in bad_message:
            try:
                # could make a function below
                bad_message = re.findall("is (.*?)<br/>", bad_message)
                bad_message = bad_message[0].split(" - ")[0].split(" ")
                earliest_year = int(bad_message[1])
                earliest_month = int(
                    datetime.datetime.strptime(bad_message[0], "%b").month
                )
                return True, [], {}, earliest_year, earliest_month, all_time_dict
            except:
                return True, [], {}, earliest_year, earliest_month, all_time_dict
    except Exception as e:
        print(e)
        pass

    # gets any update message (might need a sooner time period)
    # try:
    #    note_message = tree.xpath("/html/body/div[1]")
    #    note_message = etree.tostring(note_message[0]).decode()

    # /html/body/div[1]/div[3]/text()
    # print(note_message)
    #    if (
    #        '<div class="alert alert-primary alert-dismissible" role="alert">'
    #        in note_message
    #    ):
    # print(note_message)
    # could make a function below
    #        note_message = re.findall(
    #            '<div class="alert alert-primary alert-dismissible" role="alert">(.*?)</div>',
    #            note_message,
    #        )
    #        note_message = re.findall("\[(.*?) -", note_message[0])[0].split(" ")
    #        earliest_year = int(note_message[1]) + 1
    #        earliest_month = int(
    #           datetime.datetime.strptime(note_message[0], "%b").month
    #        )
    #        print("hi")
    #        return True, [], {}, earliest_year, earliest_month, all_time_dict
    # except Exception as e:
    #    print(note_message)
    #    pass

    # gets the maximum sharpe ratio table
    portfolio_tree = tree.xpath("//*[@id='growthChart']/div[2]/div[2]/div/div[1]/table")
    summary_tree = tree.xpath("//*[@id='growthChart']/div[3]")

    try:
        # Parses table data into tickers and %'s
        sharpe_port_from_page = etree.tostring(portfolio_tree[0])
        summary_from_page = etree.tostring(summary_tree[0])

        summary = re.findall(
            '<td class="numberCell">(.*?)</td>', str(summary_from_page)
        )

        ticker = re.findall("<td>(.*?)</td>", str(sharpe_port_from_page))
        tickers = [ticker[i] for i in range(len(ticker)) if i % 2 == 0]

        percent = re.findall(
            '<td class="numberCell">(.*?)</td>', str(sharpe_port_from_page)
        )

        for ticker in posted_tickers:
            # checks if its in the dictionary yet and then if it was on the webpage
            # last part is if we a tick with 0% and another with 100% we need
            # to a 0 into the arr for averaging purposes
            if ticker not in data_dict2:
                # Initial add of each ticker (first time scraped)
                if ticker not in tickers:

                    received_data_dict[ticker] = [0]
                else:
                    received_data_dict[ticker] = [percent[tickers.index(ticker)]]
            else:
                if ticker not in tickers:
                    temp_data_dict = data_dict2[ticker]
                    temp_data_dict.append(0)
                    received_data_dict[ticker] = temp_data_dict
                else:
                    temp_data_dict = data_dict2[ticker]
                    temp_data_dict.append(percent[tickers.index(ticker)])
                    received_data_dict[ticker] = temp_data_dict
        for pp in summary:
            try:
                ppp = pp.split("/> ")
                _summary_data.append(ppp[1])
            except:
                _summary_data.append(pp)
    except Exception as ex:
        traceback.print_exc()
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
