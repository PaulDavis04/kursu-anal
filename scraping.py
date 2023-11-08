import pandas as pd

import matplotlib.pyplot as plt
import psycopg2
import requests
from bs4 import BeautifulSoup
import numpy as np


# def lietuvos_bankas():
#     url = "https://www.lb.lt/en/daily-euro-foreign-exchange-reference-rates-published-by-the-european-central-bank"
#     response = requests.get(url)
#     # print(response)
#     soup = BeautifulSoup(response.content, "html.parser")
#     valiutu_kursai = soup.find("table", class_="table table-bordered tablesorter")
#     # print(valiutu_kursai)
#     stulpeliu_pavadinimai = table.find_all("th")
#     clean_titles = [title.text.strip() for title in stulpeliu_pavadinimai]
#     valiutos = []
#
#     rows = valiutu_kursai.find_all("tr")
#     for row in rows:
#         columns = row.find_all("td")
#         player_data = [column.text.strip() for column in columns]
#         data.append(player_data)
#
#     df = pd.DataFrame(valiutos, columns= clean_titles)
#     print(df)
#     df.to_csv("Valiutu kursai.csv", escapechar= " ", index=False)
# #####---------------

from datetime import datetime, timedelta


def currency_scraping():
    # Define the number of days to scrape
    num_days = 30
    base_date = datetime.today()
    date_list = [base_date - timedelta(days=x) for x in range(num_days)]
    # Initialize the list to hold all currency exchange data
    all_currency_exchanges = []
    # Loop over each date and scrape data
    for date in date_list:
        # Format the date as 'YYYY-MM-DD'
        date_str = date.strftime("%Y-%m-%d")
        target_url = f"https://www.lb.lt/en/daily-euro-foreign-exchange-reference-rates-published-by-the-european-central-bank?class=Eu&type=day&selected_curr=&date_day={date_str}"

        try:
            response = requests.get(target_url)
            # Ensure the request was successful
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            continue
        except Exception as e:
            print(f"Other error occurred: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'table table-bordered tablesorter'})

        # Check if the table is found
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    curr_title = cells[0].text.strip()
                    curr_rate = cells[1].text.strip()
                    curr_proportion = cells[2].text.strip().replace(',', '.').replace(' ', '')
                    curr_change = cells[3].text.strip().replace(',', '.')
                    curr_change_percentage = cells[4].text.strip().replace(',', '.').replace('%', '')
                    all_currency_exchanges.append(
                        [date_str, curr_title, curr_rate, curr_proportion, curr_change, curr_change_percentage])

    return all_currency_exchanges

currency_data = currency_scraping()
# for entry in currency_data:
#     print(entry)