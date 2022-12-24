import requests
import lxml.html as lh
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re

from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService


def spyGet():
    url = "https://www.slickcharts.com/sp500"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "referer": "https://www.slickcharts.com/sp500",
    }
    page = requests.get(url, headers=headers)
    doc = lh.fromstring(page.content)

    # r.html.find('#myElementID').text

    tr_elements = doc.xpath("//tr")

    col = []
    i = 0

    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))

    for j in range(1, len(tr_elements)):
        T = tr_elements[j]

        if len(T) != 7:
            break

        i = 0

        for t in T.iterchildren():
            data = t.text_content()
            if i > 0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i += 1  # this puts the 0-14

    Dict = {title: column for (title, column) in col}
    df = pd.DataFrame(Dict)
    df.columns = ["#", "Company", "Symbol", "Percent", "Value", "Chg", "% Chg"]

    q = 0
    p = 0

    for q in range(15):  # Is 15 because that's how many we are checking!
        x = df.iloc[q]["Symbol"]
        x = x.replace(".", "-")
        df.at[q, "Symbol"] = x

    df2 = df.loc[0:14, "Symbol":"Percent"]
    return df2


def evaulate(ticks):

    arr = np.full(
        shape=len(ticks), fill_value=round((100 / len(ticks)), 2), dtype=np.float16
    )
    total = round(round((100 / len(ticks)), 2) * len(ticks), 2)
    if total < 100:
        arr[0] += round(100 - total, 2)
    elif total > 100:
        arr[0] = round(arr[0] - (total - 100), 2)
    arr = ["".join(item) for item in arr.astype(str)]

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        options=options, service=FirefoxService(GeckoDriverManager().install())
    )

    driver.get("https://www.portfoliovisualizer.com/optimize-portfolio")
    driver.refresh()
    if len(ticks) / 10 >= 1:
        for i in range(int(len(ticks) / 10)):
            more = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(("link text", "More"))
            )
            driver.execute_script("arguments[0].click();", more)
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input"))
    )

    ticker_inputs = []
    allocation_inputs = []
    for x in elements:
        if "symbol" in x.get_attribute("name"):
            ticker_inputs.append(x)
        if "allocation" in x.get_attribute("name"):
            allocation_inputs.append(x)
    for x in range(len(ticks)):
        ticker_inputs[x].send_keys(ticks[x])
        allocation_inputs[x].send_keys(arr[x])

    optimize = driver.find_element(By.ID, "submitButton")
    driver.execute_script("arguments[0].click();", optimize)

    # /html/body/div[1]/div[6]/div[1]/div[2]/div[2]/div/div[1]/table/tbody
    # Above is Full XPATH
    # Below is XPATH
    # //*[@id="growthChart"]/div[2]/div[2]/div/div[1]/table/tbody
    output = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div[6]/div[1]/div[2]/div[2]/div/div[1]/table/tbody",
            )
        )
    )
    output = output.get_attribute("innerHTML")
    driver.close()

    ticker = re.findall("<td>(.*?)</td>", str(output))
    percent = re.findall('<td class="numberCell">(.*?)</td>', str(output))
    # for i in output.get_attribute("innerHTML").replace("</td>", "<td>").split("<td>"):
    #    print(i)

    tickers = []
    for i in range(len(ticker)):
        if i % 2 == 0:
            tickers.append(ticker[i])

    df = pd.DataFrame(tickers, columns=["Tickers"])
    df["Percents"] = percent
    return df
