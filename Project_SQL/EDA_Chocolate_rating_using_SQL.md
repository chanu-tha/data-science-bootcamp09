## This project aims to demonstrate my skill on Exploratory Data Analysis using SQL








Import dataset to ElephantSQLby using python
```python
## install library
import pandas as pd
import psycopg2

## get file from GG drive
df = pd.read_csv('/content/drive/MyDrive/Tableau_dataset/Chocolate Data/chocolate.csv')

## I leave database information blank
conn = psycopg2.connect(
    host= " ",
    port=5432,
    database=" ",
    user=" ",
    password=" "
)
cur = conn.cursor()

## create table in database
chocolate_table = """
CREATE TABLE IF NOT EXISTS chocolate (
    ref int,
    company_manufacturer varchar,
    company_location varchar,
    review_date int,
    country_of_bean_origin varchar,
    specific_bean_origin_or_bar_name varchar,
    cocoa_percent varchar,
    ingredients varchar,
    most_memorable_characteristics varchar,
    rating numeric

)
"""
cur.execute(chocolate)
conn.commit()

df.to_sql('chocolate', conn, if_exists='append', index=False)

##close connection

cur.close()
conn.close()
```




1.
