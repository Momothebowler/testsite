import pandas as pd
import datetime
import yfinance as yf
import numpy as np


def get_time_period(start_date, end_date, ticker):
    df = None
    start_date_offset = 0
    end_date_offset = 0
    while df is None:
        try:
            df = pd.read_csv(r"DataSheets/" + str(ticker) + "_DataSheet", sep="|")
            start_date_unix = datetime.datetime.strptime(
                start_date, "%Y-%m-%d"
            ).timestamp()
            adjusted_start_time = datetime.datetime.utcfromtimestamp(
                start_date_unix + start_date_offset
            ).strftime("%Y-%m-%d")

            end_date_unix = datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp()
            adjusted_end_time = datetime.datetime.utcfromtimestamp(
                end_date_unix + end_date_offset
            ).strftime("%Y-%m-%d")
            if adjusted_start_time not in df.values:
                start_date_offset += 86400

            if adjusted_end_time not in df.values:
                end_date_offset += 86400

            try:
                df = df.loc[
                    df.index[df["Date"] == adjusted_start_time][0] : df.index[
                        df["Date"] == adjusted_end_time
                    ][0]
                ]
            except Exception as e:
                df = None
        except:
            data = yf.download(ticker, group_by="Ticker", period="max", interval="1d")
            data.to_csv("DataSheets/" + ticker + "_DataSheet", "|")
    df = df.reset_index()
    df = df.drop(["index", "Adj Close", "Volume", "Open", "High", "Low"], axis=1)
    return df


def get_returns(ticker):
    df = get_time_period("2022-04-02", "2022-05-15", ticker)
    arr = np.array([])
    for index, row in df.iterrows():
        if index >= 0 and index < len(df.index) - 1:
            arr = np.append(arr, df["Close"][index + 1] / df["Close"][index] - 1)
        if index >= len(df.index) - 1:
            arr = np.append(arr, 0)

    df["Return"] = arr.tolist()

    return df


def get_X(ticker):
    df = get_returns(ticker)

    mean = df["Return"].mean()

    df["X"] = df["Return"] - mean
    return df


def get_covar(tickers):
    arr = []

    for ticker in tickers:
        arr.append(get_X(ticker))

    df = pd.DataFrame(arr[0]["X"].to_frame())
    for i in range(1, len(arr)):
        df["X + " + str(i)] = arr[i]["X"]

    df2 = df.T
    df = df2.dot(df)
    print(df / (len(df) - 1))
    return df / (len(df) - 1)


def get_correlation(tickers):
    arr = np.array([])
    for ticker in tickers:
        df = get_returns(ticker)

        arr = np.append(arr, df["Return"].std(ddof=1))

    df = pd.DataFrame(arr)
    df2 = df.T
    mat = df.dot(df2)
    covar_mat = get_covar(tickers)

    while len(covar_mat) > len(mat):
        covar_mat = covar_mat.drop(len(covar_mat) - 1)
    while len(covar_mat) < len(mat):
        mat = covar_mat.drop(len(covar_mat) - 1)

    matrix_div = pd.DataFrame(
        covar_mat.values / mat.values, index=covar_mat.index, columns=mat.index
    )
    return (matrix_div ** (1 / 2)).fillna(0)
