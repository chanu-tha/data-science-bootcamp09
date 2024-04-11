## This project aims to demonstrate my skill on Exploratory Data Analysis using SQL

dataset: (https://www.kaggle.com/datasets/joebeachcapital/chocolate-ratings)<br>
This dataset gives the ratings and quality of various chocolates from around the world

|variable|description|
|---|---|
|ref|Reference ID|
|company_manufacturer|Manufacturer name|
|company_location|Manufacturer region|
|review_date| year|
|country_of_bean_origin	|Country of origin|
|specific_bean_origin_or_bar_name|Specific bean or bar name|
|cocoa_percent|Cocoa percent (% chocolate)|
|ingredients|Ingredients, ("#" = represents the number of ingredients in the chocolate; B = Beans, S = Sugar, S* = Sweetener other than white cane or beet sugar, C = Cocoa Butter, V = Vanilla, L = Lecithin, Sa = Salt)|
|most_memorable_characteristics|Most Memorable Characteristics column is a summary review of the most memorable characteristics of that bar. Terms generally relate to anything from texture, flavor, overall opinion, etc. separated by ','|
|rating|rating between 1-5|	




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

2.Explore Impact of Specific Ingredients on Rating <br>
    I want to transform the 'ingredients' column in the first table into a single array containing all the unique ingredients used across all chocolate products. This will allow me to group the ingredients and analyze their impact on ratings, with any leading or trailing whitespace removed for easier processing.

```sql
-- ingredients
-- 1. Split ingredients column into separate rows for each ingredient
WITH split_ingredients AS (
    SELECT ref,
           company_manufacturer,
           company_location,
           review_date,
           country_of_bean_origin,
           specific_bean_origin_or_bar_name,
           cocoa_percent,
           TRIM(UNNEST(string_to_array(SPLIT_PART(ingredients,'-',2), ','))) AS ingredient,
           most_memorable_characteristics,
           rating
    FROM chocolate
)
-- 2. Group by ingredient and calculate average rating
SELECT ingredient,
        ROUND(AVG(rating),2) AS average_rating,
        COUNT(*)
FROM split_ingredients
GROUP BY ingredient
ORDER BY average_rating DESC;
```
[img4]
(B = Beans, S = Sugar, S* = Sweetener other than white cane or beet sugar, C = Cocoa Butter, V = Vanilla, L = Lecithin, Sa = Salt)

The three main ingredients for chocolate products are Beans, Sugar and Cocoa Butter. However, it hard to draw any conclusions about how each ingredient affects the overall rating of a recipe based solely on this table. The average rating for each ingredient is based on unknown recipes, and we don't know how much of each ingredient is used in each recipe. The only conclusion from this table is chocolate product that contains Beans, Sugar and Cocoa Butter recieve more average rating than other ingredients.

3. Identifying Flavor Profiles <br>
   Chocolate products from various bean origins exhibit distinct characteristics. The 'most_memorable_characteristics' column holds up to three characteristics per product. I intend to convert this data into an array format, similar to the previous one. Additionally, I want to standardize terms related to the 'nutty' profile by grouping them under 'nut,' 'nuts,' or 'nutty' and many more. Cleaning this data before further analysis is crucial to ensure accurate characterization.

```sql
-- create new table for clean data
DROP TABLE IF EXISTS character_clean;
CREATE TABLE character_clean(
        ref int,
        company_manufacturer varchar,
        company_location varchar,
        review_date int,
        country_of_bean_origin varchar,
        specific_bean_origin_or_bar_name varchar,
        cocoa_percent varchar,
        ingredients varchar,
        characteristics varchar,
        rating numeric
);
```

```sql
-- popular chocolate characteristics

CREATE TEMP TABLE split_characteristics AS
WITH split_characteristics AS (
    SELECT ref,
           company_manufacturer,
           company_location,
           review_date,
           country_of_bean_origin,
           specific_bean_origin_or_bar_name,
           cocoa_percent,
           TRIM(UNNEST(string_to_array(most_memorable_characteristics, ','))) AS characteristics,
           ingredients,
           rating
    FROM chocolate
)

SELECT * FROM split_characteristics;

UPDATE split_characteristics
SET characteristics = 'nutty'
WHERE characteristics IN ('nut', 'nuts');

UPDATE split_characteristics
SET characteristics = 'astringent'
WHERE characteristics = '%astin%';

UPDATE split_characteristics
SET characteristics = 'berry'
WHERE characteristics = 'berries';

UPDATE split_characteristics
SET characteristics = 'blackberry'
WHERE characteristics = 'blackberries';

UPDATE split_characteristics
SET characteristics = 'blueberry'
WHERE characteristics = 'blueberries';

-- many more term to group

UPDATE split_characteristics
SET characteristics = 'winey'
WHERE characteristics = 'wine';

UPDATE split_characteristics
SET characteristics = 'woody'
WHERE characteristics IN ('woodsy', 'wood');

-- 2. insert cleaned data into new table

INSERT INTO character_clean 
SELECT *
FROM split_characteristics

```
The terms of characterisric had been standardized.<br> 
Extract Top 10 general characteristics mention and average rating.
```sql
SELECT characteristic,
        Count(*) as num,
        ROUND(AVG(rating),2) as average_rating
FROM character_clean
GROUP BY characteristic
ORDER BY num DESC, average_rating
LIMIT 10;
```
[top10_img]

From this table, the most mentioned characteristics are nutty, sweet, and cocoa. The average rating for most characteristics is above 3.00, suggesting a general preference for chocolates with these attributes.  Creamy chocolates have the highest average rating (3.48), followed by cocoa (3.37) and spicy (3.32). This suggests a particular fondness for creamy chocolates, but also an appreciation for complex flavors.

While "sweet" is the second most mentioned characteristic, its ratings (3.05) are more varied than other descriptors. This suggests that people have diverse preferences for sweetness levels in chocolate, ranging from very sweet to less sweet. This complexity extends beyond sweetness, with cocoa, spicy, and roasty flavors also receiving high average ratings. This indicates that consumers appreciate chocolates with a variety of taste profiles, not just sweetness.

SQL queries can provide insights into chocolate characteristics, but a clean dataset like this one is much easier to analyze with data visualization tools. Visualization tools can uncover hidden patterns within the hundreds of characteristics listed, leading to a richer understanding of consumer preferences.


4.Find the top manufacturers that produce chocolate products with recommended rating or above<br>
|rating|description|
|---|---|
|4.0 - 5.0|Outstanding|
|3.5 - 3.9|Highly Recommended|
|3.0 - 3.49|Recommended|
|2.0 - 2.9|Disappointing|
|1.0 - 1.9|Unpleasant|


I will use the scale in the rating table to do segmentation for each product.<br>

```sql
SELECT company_manufacturer,
        company_location,
        CASE WHEN rating BETWEEN 1 AND 1.9 THEN 'unpleasant'
             WHEN rating BETWEEN 2 AND 2.9 THEN 'disappointing'
             WHEN rating BETWEEN 3 AND 3.49 THEN 'recommended'
             WHEN rating BETWEEN 3.5 AND 3.9 THEN 'highly recommended'
             WHEN rating BETWEEN 4 AND 5 THEN 'outstanding'
             ELSE 'NA' END AS rating_label,
        COUNT(*) AS num_rate        
FROM chocolate
GROUP BY 1,2,3
```
[img6]
Find the top manufacturers that produce chocolate products with recommended rating or above. Need to work with the above query as CTE.
```sql
WITH segment_rating AS (
SELECT company_manufacturer,
        company_location,
        CASE WHEN rating BETWEEN 1 AND 1.9 THEN 'unpleasant'
             WHEN rating BETWEEN 2 AND 2.9 THEN 'disappointing'
             WHEN rating BETWEEN 3 AND 3.49 THEN 'recommended'
             WHEN rating BETWEEN 3.5 AND 3.9 THEN 'highly recommended'
             WHEN rating BETWEEN 4 AND 5 THEN 'outstanding'
             ELSE 'NA' END AS rating_label,
        COUNT(*) AS num_rate        
FROM chocolate
WHERE rating >= 3
GROUP BY 1,2,3)

SELECT ROW_NUMBER() OVER (ORDER BY SUM(num_rate) DESC),
        company_manufacturer,
        SUM(num_rate) AS num_rating
FROM segment_rating
GROUP BY company_manufacturer;
```
This table provides insights into the manufacturers with the most chocolate products rated as "recommended" or higher. 
1.Soma     54 products
2.Fresco   36 products
3.Arete    31 products










