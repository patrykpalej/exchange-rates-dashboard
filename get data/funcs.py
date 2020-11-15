import requests
import pandas as pd
from datetime import timedelta


def get_data_from_range(start_date, end_date):
    days_elapsed = (end_date - start_date).days + 1
    api_key = "5bd481457d85a23c162b86870a3c7111"   # patrykpalej@gmail.com
    # api_key = "c6306de007a4cf317334f9cd73156c53"  # palej@agh.edu.pl
    # api_key = "bef18344d09a9963fda9d0c8402ace0e"   # patryk.palej@comarch.com
    
    api_curr_list = "EUR,GBP,CHF,PLN"

    # a) Create an empty df
    df = pd.DataFrame(
        columns=['USD-EUR', 'USD-GBP', 'USD-CHF', 'EUR-USD', 'EUR-GBP',
                 'EUR-CHF', 'GBP-USD', 'GBP-EUR', 'GBP-CHF', 'CHF-USD',
                 'CHF-EUR', 'CHF-GBP', 'USD-PLN', 'EUR-PLN', 'GBP-PLN',
                 'CHF-PLN'],
        index=pd.to_datetime([start_date + timedelta(days=x)
                              for x in range(days_elapsed)]))

    # b) get data
    for i in df.index.date:
        #  -- get json from API
        date_ = i.strftime("%Y-%m-%d")
        url = "http://api.currencylayer.com/historical?access_key=" \
              + api_key + "&date=" + date_ + "&currencies=" + api_curr_list \
              + "&format=1"
        resp = requests.get(url).json()
        resp_dict = {resp["date"]: resp["quotes"]}
        one_day_data = resp_dict[date_]
        # ---------

        dt = pd.to_datetime(i).date()

        # USD
        df['USD-EUR'].loc[dt] = one_day_data["USDEUR"]
        df['USD-GBP'].loc[dt] = one_day_data["USDGBP"]
        df['USD-CHF'].loc[dt] = one_day_data["USDCHF"]
        df['USD-PLN'].loc[dt] = one_day_data["USDPLN"]

        # EUR
        df['EUR-USD'].loc[dt] = 1 / one_day_data['USDEUR']
        df['EUR-GBP'].loc[dt] = one_day_data['USDGBP'] / one_day_data['USDEUR']
        df['EUR-CHF'].loc[dt] = one_day_data['USDCHF'] / one_day_data['USDEUR']
        df['EUR-PLN'].loc[dt] = one_day_data['USDPLN'] / one_day_data['USDEUR']

        # GBP
        df['GBP-USD'].loc[dt] = 1 / one_day_data['USDGBP']
        df['GBP-EUR'].loc[dt] = one_day_data['USDEUR'] / one_day_data['USDGBP']
        df['GBP-CHF'].loc[dt] = one_day_data['USDCHF'] / one_day_data['USDGBP']
        df['GBP-PLN'].loc[dt] = one_day_data['USDPLN'] / one_day_data['USDGBP']

        # CHF

        df['CHF-USD'].loc[dt] = 1 / one_day_data['USDCHF']
        df['CHF-EUR'].loc[dt] = one_day_data['USDEUR'] / one_day_data['USDCHF']
        df['CHF-GBP'].loc[dt] = one_day_data['USDGBP'] / one_day_data['USDCHF']
        df['CHF-PLN'].loc[dt] = one_day_data['USDPLN'] / one_day_data['USDCHF']

    df.index = df.index.strftime("%d.%m.%Y")
    df.index.rename("timestamp", inplace=True)

    return df
