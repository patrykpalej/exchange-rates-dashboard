import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def get_data_from_range(start_date, end_date, c):
    days_elapsed = (end_date - start_date).days + 1

    # a) Create an empty df
    df = pd.DataFrame(
        columns=['USD-EUR', 'USD-GBP', 'USD-CHF', 'EUR-USD', 'EUR-GBP',
                 'EUR-CHF', 'GBP-USD', 'GBP-EUR', 'GBP-CHF', 'CHF-USD',
                 'CHF-EUR', 'CHF-GBP', 'USD-PLN', 'EUR-PLN', 'GBP-PLN',
                 'CHF-PLN'],
        index=pd.to_datetime([start_date + timedelta(days=x)
                              for x in range(days_elapsed)]))

    # b) get data
    for i in df.index:

        dt = pd.to_datetime(i).date()
        dtm = datetime(dt.year, dt.month, dt.day)

        # USD
        curr_list = ["EUR", "GBP", "CHF", "PLN"]

        usd_whole_day_list \
            = [dict((k, c.get_rates("USD", dtm + timedelta(hours=6 * j))[k])
                    for k in curr_list) for j in range(4)]

        df['USD-EUR'].loc[dt] = np.average([_usd['EUR']
                                            for _usd in usd_whole_day_list])
        df['USD-GBP'].loc[dt] = np.average([_usd['GBP']
                                            for _usd in usd_whole_day_list])
        df['USD-CHF'].loc[dt] = np.average([_usd['CHF']
                                            for _usd in usd_whole_day_list])
        df['USD-PLN'].loc[dt] = np.average([_usd['PLN']
                                            for _usd in usd_whole_day_list])

        # EUR
        curr_list = ["USD", "GBP", "CHF", "PLN"]

        eur_whole_day_list \
            = [dict((k, c.get_rates("EUR", dtm + timedelta(hours=6 * j))[k])
                    for k in curr_list) for j in range(4)]

        df['EUR-USD'].loc[dt] = np.average([_eur['USD']
                                            for _eur in eur_whole_day_list])
        df['EUR-GBP'].loc[dt] = np.average([_eur['GBP']
                                            for _eur in eur_whole_day_list])
        df['EUR-CHF'].loc[dt] = np.average([_eur['CHF']
                                            for _eur in eur_whole_day_list])
        df['EUR-PLN'].loc[dt] = np.average([_eur['PLN']
                                            for _eur in eur_whole_day_list])

        # GBP
        curr_list = ["USD", "EUR", "CHF", "PLN"]

        gbp_whole_day_list \
            = [dict((k, c.get_rates("GBP", dtm + timedelta(hours=6 * j))[k])
                    for k in curr_list) for j in range(4)]

        df['GBP-USD'].loc[dt] = np.average([_gbp['USD']
                                            for _gbp in gbp_whole_day_list])
        df['GBP-EUR'].loc[dt] = np.average([_gbp['EUR']
                                            for _gbp in gbp_whole_day_list])
        df['GBP-CHF'].loc[dt] = np.average([_gbp['CHF']
                                            for _gbp in gbp_whole_day_list])
        df['GBP-PLN'].loc[dt] = np.average([_gbp['PLN']
                                            for _gbp in gbp_whole_day_list])

        # CHF
        curr_list = ["USD", "EUR", "GBP", "PLN"]

        chf_whole_day_list \
            = [dict((k, c.get_rates("CHF", dtm + timedelta(hours=6 * j))[k])
                    for k in curr_list) for j in range(4)]

        df['CHF-USD'].loc[dt] = np.average([_chf['USD']
                                            for _chf in chf_whole_day_list])
        df['CHF-EUR'].loc[dt] = np.average([_chf['EUR']
                                            for _chf in chf_whole_day_list])
        df['CHF-GBP'].loc[dt] = np.average([_chf['GBP']
                                            for _chf in chf_whole_day_list])
        df['CHF-PLN'].loc[dt] = np.average([_chf['PLN']
                                            for _chf in chf_whole_day_list])

    df.index = df.index.strftime("%d.%m.%Y")
    df.index.rename("timestamp", inplace=True)

    return df


def get_data_until_today(start_date, end_date, c):

    return 1
