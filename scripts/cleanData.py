import pandas as pd

data = pd.read_csv('/Users/arun/Documents/Telecom Ticket Analysis/data/Telecom_Data_eng.csv')

# filter out rows where 'language' is 'de'
data = data[data['language'] != 'de']

data = data.drop(columns=['language'])

data.to_csv('/Users/arun/Documents/Telecom Ticket Analysis/data/clean_data.csv', index=False)