from datetime import date
from forex_python.converter import CurrencyRates

from funcs import get_data_from_range


c = CurrencyRates()

start_date = date(2010, 9, 21)
end_date = date(2010, 9, 23)

df = get_data_from_range(start_date, end_date, c)

file_name = start_date.strftime("%d.%m.%y") + " - " \
            + end_date.strftime("%d.%m.%y") + ".csv"

df.to_csv("../data/"+file_name, sep=';')
