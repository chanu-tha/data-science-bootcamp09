This is a pratical exam for SQL Associate with 4 Tasks to be completed.

**My comment will be in bold**

## Practical Exam:Hotel Operations

LuxurStay Hotels is a major, international chain of hotels. They offer hotels for both business and leisure travellers in major cities across the world. The chain prides themselves on the level of customer service that they offer. 

However, the management has been receiving complaints about slow room service in some hotel branches. As these complaints are impacting the customer satisfaction rates, it has become a serious issue. Recent data shows that customer satisfaction has dropped from the 4.5 rating that they expect. 

You are working with the Head of Operations to identify possible causes and hotel branches with the worst problems. 
[![ER.jpg](https://i.postimg.cc/vmGYPJXT/ER.jpg)](https://postimg.cc/JsdC0dfC)

## Data

The following schema diagram shows the tables available. You have only been provided with data where customers provided a feedback rating.

# Task 1

Before you can start any analysis, you need to confirm that the data is accurate and reflects what you expect to see. 

It is known that there are some issues with the `branch` table, and the data team have provided the following data description. 

Write a query to return data matching this description. You must match all column names and description criteria.

| Column Name | Criteria                                                |
|-------------|---------------------------------------------------------|
|id | Nominal. The unique identifier of the hotel. </br>Missing values are not possible due to the database structure.|
| location | Nominal. The location of the particular hotel. One of four possible values, 'EMEA', 'NA', 'LATAM' and 'APAC'. </br>Missing values should be replaced with “Unknown”. |
| total_rooms | Discrete. The total number of rooms in the hotel. Must be a positive integer between 1 and 400. </br>Missing values should be replaced with the default number of rooms, 100. |
| staff_count | Discrete. The number of staff employeed in the hotel service department. </br>Missing values should be replaced with the total_rooms multiplied by 1.5. |
| opening_date | Discrete. The year in which the hotel opened. This can be any value between 2000 and 2023. </br>Missing values should be replaced with 2023. |
| target_guests | Nominal. The primary type of guest that is expected to use the hotel. Can be one of 'Leisure' or 'Business'. </br>Missing values should be replaced with 'Leisure'. |

**Write query to explore the branch table**


```SQL
SELECT *
FROM branch;
```
**The result showed**
[![1.jpg](https://i.postimg.cc/PfDr65y2/1.jpg)](https://postimg.cc/Wt2vzjQk)
[![2.jpg](https://i.postimg.cc/HxyHP6wV/2.jpg)](https://postimg.cc/CBSWRH6g)

**According to the result, the table need to be cleaned. The column 'total_rooms' contains NULL value and need to be replaced with 100, 
column 'opening_date' contains '-' and need to be replaced with '2023',
column 'target_guests' contains 'B.' and need to be replaced with 'Business' as below query**

```SQL
SELECT  id::text,
		location,
		Coalesce(total_rooms, 100) AS total_rooms,
		staff_count,
		REPLACE(opening_date,'-', '2023')::integer AS opening_date,
		REPLACE(target_guests,'B.', 'Business') AS target_guests
FROM branch;
```


# Task 2

The Head of Operations wants to know whether there is a difference in time taken to respond to a customer request in each hotel. They already know that different services take different lengths of time. 

Calculate the average and maximum duration for each branch and service. Your output should include the columns `service_id`, `branch_id`, `avg_time_taken` and `max_time_taken`. Values should be rounded to two decimal places where appropriate. 

**From this task, I need to extract 'service_id', 'branch_id and aggregate value to find average time and maximum duration service time as query below**

```SQL
SELECT
		service_id,
		branch_id,
		ROUND(AVG(time_taken),2) AS avg_time_taken,
		MAX(time_taken) AS max_time_taken
FROM request
GROUP BY service_id, branch_id;
```

**The result showed**
[![3.jpg](https://i.postimg.cc/W4ts0Ntm/3.jpg)](https://postimg.cc/B89W0GTt)


# Task 3

The management team want to target improvements in `Meal` and `Laundry` service in Europe (`EMEA`) and Latin America (`LATAM`). 

Write a query to return the `description` of the service, the `id` and `location` of the branch, the id of the request as `request_id` and the `rating` for the services and locations of interest to the management team. 

**From this task, I need to join 3 tables together to get data requested from management team as query below**

```SQL
SELECT
		se.description,
		b.id,
		b.location,
		re.id AS request_id,
		re.rating
FROM service se
JOIN request re
ON re.service_id = se.id
-- subquerie only location in 'EMMA' and 'LATAM'
JOIN (SELECT id, location FROM branch 
		  WHERE location IN ('EMEA','LATAM')) as b
ON re.branch_id = b.id
-- filter description only 'Meal' and 'Laundry'
WHERE se.description in ('Meal','Laundry');
```
**The result showed**
[![4.jpg](https://i.postimg.cc/zfM8jsRs/4.jpg)](https://postimg.cc/8Fh2kn44)

# Task 4

So that you can take a more detailed look at the lowest performing hotels, you want to get service and branch information where the average rating for the branch and service combination is lower than 4.5 - the target set by management.  

Your query should return the `service_id` and `branch_id`, and the average rating (`avg_rating`), rounded to 2 decimal places.

**For this task, I filtered the average rating for combination of branches and services by query below**

```SQL
SELECT
		service_id,
		branch_id,
		ROUND(AVG(rating),2) AS avg_rating
FROM request
GROUP BY service_id, branch_id

-- filter only rating lower than 4.5
HAVING ROUND(AVG(rating),2) < 4.5
ORDER BY avg_rating ASC;

**The result showed**

```
**The result shows**
[![5.jpg](https://i.postimg.cc/G3BCjFGZ/5.jpg)](https://postimg.cc/9zjKmqxp)
