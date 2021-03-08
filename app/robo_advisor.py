import requests 

import json
import csv 
import os

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

#info inputs 

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

#latest day
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#latest closing price 
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #assumes latest day is on top
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

#get high price from each day
high_prices = []
for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))

#maximum of high prices
recent_high = max(high_prices)

#get low price from each day
low_prices = []
for date in dates:
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

#min of low prices
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "...", "data", "prices.csv")


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

