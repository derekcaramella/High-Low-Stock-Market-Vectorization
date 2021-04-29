import numpy as np
import pandas as pd
import bs4
import urllib.request as urllib2


def retrieve_historical_stock_data(stock_ticker, base_date, end_date):
    """"The function will return a pandas DataFrame - position 1 is the date & position 2 is open USD price."""
    stock_data = []
    url = 'https://finance.yahoo.com/quote/' + stock_ticker + '/history/'
    rows = bs4.BeautifulSoup(urllib2.urlopen(url).read(), features='html.parser').findAll('table')[0].tbody.findAll(
        'tr')
    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text != 'Dividend':  # Ignore this row in the table
            stock_data.append((divs[0].span.text, float(divs[1].span.text.replace(',', ''))))
    df = pd.DataFrame(stock_data, columns=['Date', 'Open USD Price'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df[(df['Date'] >= base_date) & (df['Date'] <= end_date)]


aapl_open_prices = retrieve_historical_stock_data('AAPL', '2021-04-23', '2021-04-27')
print(aapl_open_prices.apply(lambda row: [row['Date'].strftime('%Y-%m-%d'),
                                          row['Open USD Price'] - int(aapl_open_prices['Open USD Price'].iloc[1])]
if row['Date'] > aapl_open_prices['Date'].iloc[1] else [row['Date'].strftime('%Y-%m-%d'), 0],
                             axis=1))


# k = len(aapl_open_prices)
# while k >= 0:
#     if k == len(aapl_open_prices):
#         aapl_open_prices['Profit'] = aapl_open_prices.apply(lambda row: row - aapl_open_prices.iloc[[k-1]].values[0], axis=1)
#     else:
#         aapl_open_prices.append(aapl_open_prices.apply(lambda row: row - aapl_open_prices.iloc[[1]].values[0], axis=1))
#
#     print(aapl_open_prices)
#     k = k-1
#     print(k)

# print(aapl_open_prices)
