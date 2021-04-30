# Import packages
import pandas as pd
import plotly.graph_objects as go
import bs4
import urllib.request as urllib2


def retrieve_historical_stock_data(stock_ticker, base_date, end_date):
    """"The function will return a pandas DataFrame - position 1 is the date & position 2 is open USD price."""
    stock_data = []  # Empty list for the dataframe return
    url = 'https://finance.yahoo.com/quote/' + stock_ticker + '/history/'  # Retrieval url from tick parameter
    # Load historical rows of data from url
    rows = bs4.BeautifulSoup(urllib2.urlopen(url).read(), features='html.parser').findAll('table')[0].tbody.findAll(
        'tr')
    for each_row in rows:  # Parse each row for information
        divs = each_row.findAll('td')  # td is the html subcomponent of html tr in a table
        if divs[1].span.text != 'Dividend':  # Ignore this row in the table
            #  Grab text in these positions & remove comma from thousand number values; then, append tuple to list
            stock_data.append((divs[0].span.text, float(divs[1].span.text.replace(',', ''))))
    df = pd.DataFrame(stock_data, columns=['Date', 'Open USD Price'])  # Convert list of tuples to a data frame
    df['Date'] = pd.to_datetime(df['Date'])  # Convert string dates to datetime objects for the data frame
    return df[(df['Date'] >= base_date) & (df['Date'] <= end_date)]  # Filtered data frame dependant on parameters


# Execute function for Apple from January 1, 2021 to April 4, 2021
aapl_open_prices = retrieve_historical_stock_data('AAPL', '2021-01-01', '2021-04-29')
percent_change_df = pd.DataFrame()  # Create an empty data frame to append lambda data
#  For loop in reverse order to calculate from the bottom up the percentage changes. Use the length for robustness
for x in reversed(range(0, len(aapl_open_prices))):
    # Create three columns: Purchase Date, Sell Date, & Percent Change. For the given row, loop through all rows in the
    # data frame, if the row's date is greater than the looped row, then return 0 because in the stock market that
    # instance cannot occur. Else, return the percentage change between the given row and looped row. Expand the
    # return to three columns.
    aapl_open_prices[['Purchase Date', 'Sell Date', 'Percent Change']] = aapl_open_prices.apply(
        lambda row: [aapl_open_prices['Date'].iloc[x].strftime('%Y-%m-%d'), row['Date'].strftime('%Y-%m-%d'),
                     ((row['Open USD Price'] - aapl_open_prices['Open USD Price'].iloc[x]) /
                      aapl_open_prices['Open USD Price'].iloc[x])*100]
        if row['Date'] > aapl_open_prices['Date'].iloc[x] else [aapl_open_prices['Date'].iloc[x].strftime('%Y-%m-%d'),
                                                                row['Date'].strftime('%Y-%m-%d'), 0],
        axis=1, result_type='expand')
    percent_change_df = percent_change_df.append(aapl_open_prices)  # Append instance result to larger data frame

fig = go.Figure(data=go.Heatmap(x=percent_change_df['Purchase Date'],  # x-axis is the Purchase Date
                                y=percent_change_df['Sell Date'],  # y-axis is the Sell Date
                                z=percent_change_df['Percent Change'],  # The depth is the percentage change
                                colorscale='RdBu'))  # The color scale is bipolar, which highlights the plus/minus
fig.update_layout(title='Apple Capital Gains Yield',  # Set the title
                  title_x=0.5,  # Position the title in the middle of the graph
                  title_y=0.92,  # Set the distance between the graph & title
                  font=dict(family='Times New Roman, Times New Roman'))  # Set font, title & body
fig.update_xaxes(title_text='Purchase Date')  # Set x-axis title
fig.update_yaxes(title_text='Sell Date')  # Set y-axis title

fig.show()  # Show graph
