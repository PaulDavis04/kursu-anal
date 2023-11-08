import pandas as pd

import matplotlib.pyplot as plt
import psycopg2
import requests
from bs4 import BeautifulSoup
from db_config import select_currency_data, connect_db
# from scraping import currency_scraping
####
def currency_dataframe():
    table_name = "currency_rates"
    currency_data = select_currency_data(connect_db(), table_name)

    if currency_data:
        data = pd.DataFrame(currency_data, columns=['Data','Title', 'Currency Code', 'Proportion', 'Change', 'Change %'])
        try:
            # print(data)
            return data
        except ValueError as e:
            print(f"DataFrame is Empty! {e}")
    else:
        print("No data was scraped!")
    return pd.DataFrame()


# currency_dataframe()