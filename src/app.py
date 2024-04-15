import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns



url = "https://ycharts.com/companies/TSLA/revenues"
html_data = requests.get(url, time.sleep(10)).text

if "403 ERROR" in html_data:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    #headers = {"Users-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36)"}

    html_data = requests.get(url, headers=headers)
    time.sleep(10)
    html_data = html_data.text

html_data


soup = BeautifulSoup(html_data, 'html.parser')
soup

tables = soup.find_all('table')
tables

for index, table in enumerate(tables):
    if ("Date" in str(table)):
        table_index = index
        break
    print(table)
table_index

import pandas as pd

tesla_df = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].find_all('tr'):
    col = row.find_all('td')
    if (col != []):
        date = col[0].text
        revenue = float(col[1].text.strip().replace('B',''))
        tesla_df = pd.concat([tesla_df, pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])], ignore_index=True)
                                                                                
tesla_df

import sqlite3
conn = sqlite3.connect('tesla.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS tesla_revenue (date TEXT, revenue REAL)')
conn.commit()

tesla_df.to_sql('tesla_revenue', conn, if_exists='replace', index = False)


c.execute('SELECT * FROM tesla_revenue').fetchall()

import matplotlib.pyplot as plt
import seaborn as sns

tesla_df['Date'] = pd.to_datetime(tesla_df['Date'])

sns.lineplot(x='Date', y='Revenue', data=tesla_df)
plt.title("Tesla Revenue Over TIme")
plt.xticks(rotation=45)
plt.show()


plt.scatter(tesla_df['Date'], tesla_df['Revenue'])
plt.title("Tesla Revenue Over TIme")
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()