## Practical Exam for Data Analyst Associate certification on Datacamp

**My comments will be in Bold**

### Grocery Store Sale

The data is available in the table `products`.

The dataset contains records of customers for their last full year of the loyalty program.

| Column Name | Criteria                                                |
|-------------|---------------------------------------------------------|
|product_id | Nominal. The unique identifier of the product. </br>Missing values are not possible due to the database structure.|
| product_type | Nominal. The product category type of the product, one of 5 values (Produce, Meat, Dairy, Bakery, Snacks). </br>Missing values should be replaced with “Unknown”. |
| brand | Nominal. The brand of the product. One of 7 possible values. </br>Missing values should be replaced with “Unknown”. |
| weight | Continuous. The weight of the product in grams. This can be any positive value, rounded to 2 decimal places. </br>Missing values should be replaced with the overall median weight. |
| price | Continuous. The price the product is sold at, in US dollars. This can be any positive value, rounded to 2 decimal places. </br>Missing values should be replaced with the overall median price. |
| average_units_sold | Discrete. The average number of units sold each month. This can be any positive integer value. </br>Missing values should be replaced with 0. |
| year_added | Nominal. The year the product was first added to FoodYum stock.</br>Missing values should be replaced with 2022. |
| stock_location | Nominal. The location that stock originates. This can be one of four warehouse locations, A, B, C or D </br>Missing values should be replaced with “Unknown”. |

# Task 1

Last year (2022) there was a bug in the product system. For some products that were added in that year, the `year_added` value was not set in the data. As the year the product was added may have an impact on the price of the product, this is important information to have. 

Write a query to determine how many products have the `year_added` value missing. Your output should be a single column, `missing_year`, with a single row giving the number of missing values.

**I started with explore the data**

```SQL
SELECT *
FROM products;
```

**As I can see from the table, the 'year_added' column has many NULL value. From Task 1, they asked to count the NULL values as missing_year which can do by the query below**

```SQL
SELECT Count(*) AS missing_year
FROM products
WHERE year_added IS NULL;
```

**The result is there are 170 missing values from 'year_added' column**




# Task 2

Given what you know about the year added data, you need to make sure all of the data is clean before you start your analysis. The table below shows what the data should look like. 

Write a query to ensure the product data matches the description provided. Do not update the original table.  

| Column Name | Criteria                                                |
|-------------|---------------------------------------------------------|
|product_id | Nominal. The unique identifier of the product. </br>Missing values are not possible due to the database structure.|
| product_type | Nominal. The product category type of the product, one of 5 values (Produce, Meat, Dairy, Bakery, Snacks). </br>Missing values should be replaced with “Unknown”. |
| brand | Nominal. The brand of the product. One of 7 possible values. </br>Missing values should be replaced with “Unknown”. |
| weight | Continuous. The weight of the product in grams. This can be any positive value, rounded to 2 decimal places. </br>Missing values should be replaced with the overall median weight. |
| price | Continuous. The price the product is sold at, in US dollars. This can be any positive value, rounded to 2 decimal places. </br>Missing values should be replaced with the overall median price. |
| average_units_sold | Discrete. The average number of units sold each month. This can be any positive integer value. </br>Missing values should be replaced with 0. |
| year_added | Nominal. The year the product was first added to FoodYum stock.</br>Missing values should be replaced with last year (2022). |
| stock_location | Nominal. The location that stock originates. This can be one of four warehouse locations, A, B, C or D </br>Missing values should be replaced with “Unknown”. |

**First, I write the query to check on each column whether if it contains any missing value or not**

```SQL
SELECT 
	SUM(CASE WHEN product_type IS NULL THEN 1 ELSE 0 END) AS product_type_null,
	SUM(CASE WHEN brand IS NULL THEN 1 ELSE 0 END) AS brand_null,
	SUM(CASE WHEN year_added IS NULL THEN 1 ELSE 0 END) AS year_added_null,
	SUM(CASE WHEN weight IS NULL THEN 1 ELSE 0 END) AS weight_null,
	SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS price_null,
	SUM(CASE WHEN weight IS NULL THEN 1 ELSE 0 END) AS weight_null,
	SUM(CASE WHEN average_units_sold IS NULL THEN 1 ELSE 0 END) AS average_units_sold_null,
	SUM(CASE WHEN stock_location IS NULL THEN 1 ELSE 0 END) AS stock_location_null,
	Count(DISTINCT brand) AS brand_cnt,
	Count(DISTINCT product_type) AS product_type_cnt
	
	
FROM products;
```

**The result gives that only 'year_added' that has missing value. However, there are some other columns that need to be clean.**
- __'brand' column needs to replace '-' to 'Unknown'.__
- __'weight' column needs to replace 'grams ' and round into 2 decimal places.__
- __'price' column needs to round into 2 decimal places.__
- __'average_units_sold' needs to be positive integer.__
- __'year_added' needs to replace NULL value with 2022.__
- __'stock location' needs to uppercase letter.__

```SQL
DROP TABLE IF EXISTS products_clean;

CREATE TEMP TABLE products_clean AS
WITH pro_wt AS (SELECT product_id,
			  ROUND(REPLACE(weight, ' grams', '')::NUMERIC,2) AS weight 
			  FROM products)
			
SELECT products.product_id,
       COALESCE(product_type, 'Unknown') AS product_type,
       COALESCE(brand, 'Unknown') AS brand,
	     COALESCE(pro_wt.weight, (SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY pro_wt.weight)
                              FROM pro_wt)) AS weight,
	     COALESCE(ROUND(price::numeric,2), (SELECT ROUND(percentile_cont(0.5)
                              WITHIN GROUP (ORDER BY price)::numeric,2)
                              FROM products)) AS price,
       COALESCE(ABS(average_units_sold::integer), 0) AS average_units_sold,
       COALESCE(year_added, '2022') AS year_added,
       COALESCE(UPPER(stock_location), 'Unknown') AS stock_location
FROM products

-- Join with pro_wt table
INNER JOIN pro_wt
ON products.product_id = pro_wt.product_id;

SELECT * FROM products_clean;
```

# Task 3

To find out how the range varies for each product type, your manager has asked you to determine the minimum and maximum values for each product type.   

Write a query to return the `product_type`, `min_price` and `max_price` columns. 

**For Task 3, it seems to be quite straightforward, using and aggregate function to find min and max price to get answer**

```SQL
SELECT product_type,
	Min(price) AS min_price,
	Max(price) AS max_price
FROM products
GROUP BY product_type;
```

**The result shows**



# Task 4

The team want to look in more detail at meat and dairy products where the average units sold was greater than ten. 

Write a query to return the `product_id`, `price` and `average_units_sold` of the rows of interest to the team. 

**For Task 4, I need to use WHERE clause to filter for the condition: product_type needs to be Meat or Dairy and average_units_sold greater than 10**

```SQL
SELECT product_id,
	price,
	average_units_sold
FROM products
WHERE product_type IN ('Meat', 'Dairy') AND average_units_sold > 10;
```

**The result shows**


