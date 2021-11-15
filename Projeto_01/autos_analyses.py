"""
project made by Mateus Eloi Bastos :)
"""

# Importing the libraries
import pandas as pd

# reading a csv file
autos = pd.read_csv("autos.csv", encoding='Latin-1')

# renaming some coluns
autos.columns=['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_pictures', 'postal_code',
       'last_seen']

# columns that have mostly one value that are candidates to be dropped
# pylint: disable=E1101
autos = autos.drop(columns=['num_pictures', 'offer_type','seller'], axis=1)

'''
Price and odometer columns are numeric values stored as text. For each column:
- Remove any non-numeric characters.
- Convert the column to a numeric dtype.
'''
autos.price = [value.replace('$','').replace(',','') for value in autos.price]
autos.odometer = [value.replace('km','').replace(',','') for value in autos.odometer]

autos.price = pd.to_numeric(autos.price)
autos.odometer = pd.to_numeric(autos.odometer)

# renaming the column to odometer_km
autos.rename(columns={'odometer':'odometer_km'}, inplace=True)

# Removing the outliers, 1 < values < 350000
autos = autos[autos.price.between(1,350000)]

''' Calculate the distribution of values in the date_crawled,
ad_created, and last_seen columns (all string columns)
as percentages '''
autos['date_crawled'].str[:10].value_counts(normalize=True, dropna=False).sort_index()
autos['ad_created'].str[:10].value_counts(normalize=True, dropna=False).sort_index()
autos['last_seen'].str[:10].value_counts(normalize=True, dropna=False).sort_index()

# dropping values outside acceptable range (between 1910 and 2016)
autos = autos[autos.registration_year.between(1910,2016)]

#  selecting the top 20
first_20_brands = autos.brand.value_counts().head(20).index

# Aggregating the mean of km and prices
dict_agg_brand={}
dict_agg_km={}
for brand in first_20_brands:
    mean_price_brand = autos[autos['brand']==brand]['price'].mean()
    mean_km_brand = autos[autos['brand']==brand]['odometer_km'].mean()
    dict_agg_brand[brand]=mean_price_brand
    dict_agg_km[brand]=mean_km_brand

#Creating the final dataframe!
brand_mean_series = pd.Series(dict_agg_brand)
km_mean_series = pd.Series(dict_agg_km)

df_brand_mean = pd.DataFrame(brand_mean_series, columns=['mean_price'])
df_brand_mean['mean_km'] = km_mean_series

print('Finished!')
