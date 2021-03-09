#collaborated with Patrick Lazzaro on this project
import requests 
from dotenv import load_dotenv

import json
import csv 
import os

load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

#user inputs and validation
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
while True:
    symbol = input("HELLO! PLEASE ENTER A STOCK SYMBOL/TICKER (ex. AAPL):")

    if (hasNumbers(symbol) == True) or (len(symbol) >5) or (len(symbol) <1):
        print("OOPS, please choose a valid stock symbol and try again!")
    else:
        break

#API key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

#post get request validation
if "Error Message" in response.text:
    print("Sorry, couldn't find any trading data for that stock symbol. Please try again!")
    exit()

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

#csv data 
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
        "timestamp": date,
        "open": daily_prices["1. open"], 
        "high": daily_prices["2. high"], 
        "low": daily_prices["3. low"], 
        "close": daily_prices["4. close"], 
        "volume": daily_prices["5. volume"]
    })

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

#request time
import datetime
now = datetime.datetime.now()
print("REQUEST AT: " + str(now.strftime("%Y-%m-%d %I:%M %p")))

#latest day, close, high, low
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")

#recommendation
if (float(latest_close) >= (recent_high* .90)):
    recommendation = "STRONG BUY"
    reason = "The stock price is within 10% of its recent high."
elif (float(latest_close) >= (recent_high* .80)) & (float(latest_close) < (recent_high* .90)):
    recommendation = "BUY"
    reason = "The stock price is within 10-20% of its recent high."
elif (float(latest_close) >= (recent_high* .65)) & (float(latest_close) < (recent_high* .80)):
    recommendation = "HOLD"
    reason = "The stock price is within 20-35% of its recent high."
elif (float(latest_close) >= (recent_high* .50)) & (float(latest_close) < (recent_high* .65)):
    recommendation = "SELL"
    reason = "The stock price is within 35-50% of its recent high. Unless you beleive the stock is undervalued, I would not invest."
else:
    recommendation = "STRONG SELL"
    reason = "The stock is below 50% of its recent high. Unless you beleive the stock is undervalued, I would not invest."
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")

#csv and ending message
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

