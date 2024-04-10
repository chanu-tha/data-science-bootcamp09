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
Quickly view through the table
[img1]


1.Find Top-Rated Chocolate by Origin and Cocoa Percentage
```sql
--Top rated chocolate by Origin and Cocoa Percentage
SELECT country_of_bean_origin,
        cocoa_percent,
        company_manufacturer,
        ROUND(AVG(rating),2) as average_rating
FROM chocolate
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 100;
```
[img1]

I want to know more on among chocolates with a 4.0 rating, what country of origin has the highest count of beans used?

```sql
SELECT country_of_bean_origin,
        rating as rating_of_4,
        Count(*) as num,
        ROUND(Count(*)*100.0/(SELECT Count(*) from chocolate 
                        WHERE rating = 4.0),2) as proportion_pct
FROM chocolate
WHERE rating = 4.0
GROUP BY 1,2
ORDER BY 3 DESC;
```
[img2]

    The top 3 countries of bean origin
    1.Venezuela    17.86%
    2.Peru         16.96%
    3.Madagascar    9.82%

Let explore more on the corelation between cocoa percentage and rating. The column cocoa_percentage is string, it needs to convert from string to integer before finding corelation.
```sql
-- correlation between cocoa percentage and rating 
WITH cocoa_int AS (
    SELECT ref,
            substring(cocoa_percent FROM 1 FOR 2)::int AS cocoa_percent_int
    FROM chocolate
)

SELECT corr(cocoa_int.cocoa_percent_int, rating)
FROM chocolate
JOIN cocoa_int
ON chocolate.ref = cocoa_int.ref;
```
[img3]

The weak correlation (r = 0.054) between cocoa percentage and rating suggests no clear link. A scatter plot would visually confirm this.

2.
















