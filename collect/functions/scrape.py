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


def evaulate():
    tickers = ["TSLA", "AMZN", "AAPL", "GOOG", "NOK", "BBBY", "GME"]
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

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get("https://www.portfoliovisualizer.com/optimize-portfolio")
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
    print(elements)
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
    driver.quit()

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
