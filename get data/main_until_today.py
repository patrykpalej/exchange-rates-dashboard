import pandas as pd
from datetime import date, datetime
from forex_python.converter import CurrencyRates

from funcs import get_data_until_today


c = CurrencyRates()
df_pre = pd.read_csv("exchange_rates.csv", sep=';')

start_date = df_pre["timestamp"].iloc[-1]
end_date = datetime.now()

df_new = get_data_until_today(start_date, end_date, c)
df = df_pre + df_new

df.to_csv("exchange_rates.csv", sep=';')
