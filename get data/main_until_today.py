import pandas as pd
from datetime import datetime, timedelta
from forex_python.converter import CurrencyRates

from funcs import get_data_from_range


c = CurrencyRates()
df_pre = pd.read_csv("../data/exchange_rates.csv", sep=';',
                     index_col="timestamp")

start_date = datetime.date(datetime.strptime(df_pre.index[-1], "%d.%m.%Y")
                           + timedelta(days=1))
end_date = datetime.date(datetime.now())

df_new = get_data_from_range(start_date, end_date, c)
df = pd.concat([df_pre, df_new])

df.to_csv("../data/exchange_rates.csv", sep=';')
