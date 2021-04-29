import numpy as np
import bs4 as bs
import urllib.request as urllib2


data = []
url = 'https://finance.yahoo.com/quote/AAPL/history/'
rows = bs.BeautifulSoup(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
for each_row in rows:
        divs = each_row.findAll('td')
        print(divs)
        if divs[1].span.text != 'Dividend':  # Ignore this row in the table
            # I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
            data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',', ''))})
# print(data)
