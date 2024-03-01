## HOMEWORK 2

# import module
import pandas as pd
from requests import get
from time import sleep


beer_url = "https://api.punkapi.com/v2/beers"
resp = get(beer_url)

#check response
print(resp.status_code)
beer_list = []

for i in range(len(resp.json())):
  beer_resp = resp.json()[i]
  beer_list.append(beer_resp)

df_beer_list = pd.DataFrame(beer_list)
print(df_beer_list.head())
df_beer_list.to_json("beer_list.json")
