from funcs import get_correlation
import time

start = time.time()

tickers = [
    "IXN",
    "BTEK",
    "IOO",
    "IWX",
    "IWY",
    "IVE",
    "IVW",
    "IJJ",
    "IJK",
    "IJS",
    "IJT",
    "IEMG",
    "IEFA",
    "REZ",
    "USRT",
    "REET",
    "TLT",
    "TLH",
    "IEI",
    "IEF",
    "SHY",
    "IGLB",
    "IGIB",
    "IGSB",
    "HYXF",
    "USHY",
    "IAGG",
    "HYXU",
    "SGOV",
]

print(get_correlation(tickers))

end = time.time()

print(end - start)
