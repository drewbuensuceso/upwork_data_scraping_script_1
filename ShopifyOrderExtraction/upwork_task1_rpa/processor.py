import requests
from datetime import datetime as dt
import pytz
import pandas as pd

DATE_TODAY = dt.now(pytz.timezone("Asia/Manila")).date() 
END_DATE = DATE_TODAY.strftime("%Y/%m/%d")
START_DATE_1 = "2000/01/01"
START_DATE_2 = "2005/01/01"
START_DATE_3 = "2010/01/01"
START_DATE_4 = "2015/01/01"
START_DATE_5 = "2020/01/01"



def process(response, symbol):
    historical_data = response.get("html")
    historical_data_list = historical_data.split("<tr>")

    data = []
    no_data = []

    for i in range(0, len(historical_data_list)):
        if len(historical_data_list[i]) == 0:
            print("no data", symbol)
            # print(historical_data)
            no_data.append({"symbol": symbol, "historical_data": historical_data})
        else:
            date = historical_data_list[i].strip("<td class=mod-ui-table__cell--text><span class=mod-ui-hide-small-below>").split("</span>")[1].split(",")
            date = date[1] + date[2]
            values = historical_data_list[i].strip("<td class=mod-ui-table__cell--text><span class=mod-ui-hide-small-below>").split("</span>")[2].split("<td>")
            datum = {
                "ISIN": symbol,
                "date": date,
                "open": values[1].strip("</td>"),
                "high": values[2].strip("</td>"),
                "low": values[3].strip("</td>"),
                "close": values[4].strip("</td>"),
                "volume": "--"
            }
            print(datum)
            data.append(datum)
    
    return data, no_data


symbol_list = pd.read_csv(f"ISINs_{DATE_TODAY}/xid_list.csv")

output_data = []
for index, row in symbol_list.iterrows():
    urls = []
    symbol = row[0]
    xid = row[1]
    URL_1 = f"https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={START_DATE_1}&endDate={START_DATE_2}&symbol={xid}"
    URL_2 = f"https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={START_DATE_2}&endDate={START_DATE_3}&symbol={xid}"
    URL_3 = f"https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={START_DATE_3}&endDate={START_DATE_4}&symbol={xid}"
    URL_4 = f"https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={START_DATE_4}&endDate={START_DATE_5}&symbol={xid}"
    URL_5 = f"https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate={START_DATE_5}&endDate={END_DATE}&symbol={xid}"
    urls.append(URL_1)
    urls.append(URL_2)
    urls.append(URL_3)
    urls.append(URL_4)
    urls.append(URL_5)
    no_data = []
    no_data_with_html = []
    for url in urls:
        try:
            response = requests.get(url)
            data = response.json()
            data, no_data = process(data, symbol)
            output_data += data
            no_data_with_html += no_data
        except Exception as e:
            print(e)
            print(f"{url} has no data")
            no_data.append({
                "xid": xid,
                "url": url
                })
print("no data for the ff ISINs", no_data)
output_data = pd.DataFrame(data=output_data)
output_data.to_csv(f"consolidate_data_{DATE_TODAY}.csv", index=False)
no_data = pd.DataFrame(data=no_data)
no_data.to_csv("queries with no data.csv")
no_data_with_html.to_csv("no_data_but_with_html.csv")