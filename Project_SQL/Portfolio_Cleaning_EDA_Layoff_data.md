## SQL Project: Cleaning and EDA on layoff dataset

**Data Dictionary**
|variable|description|
|---|---|
|company|Name of the company|
|location|Location of the company headquarters|
|industry|Industry of the company|
|total_laid_off| Number of employees laid off|
|percentage_laid_off|Percentage of employees laid off|
|date|Date of layoff|
|stage|Stage of funding|
|country|Country|
|funds_raised|Funds raised by the company (Millions USD)|


```
SELECT * FROM ;
```


### Check duplication
```sql
WITH duplicate_check as(
	SELECT
		*,
		ROW_NUMBER() OVER(PARTITION BY 	company,
						location,
						industry,
						total_laid_off,
						percentage_laid_off,
						`date`,
						stage,
						country,
						funds_raised) - 1 AS duplicate
		
	FROM layoffs_wk)
SELECT * 
FROM duplicate_check
WHERE duplicate > 0;

SELECT * 
FROM duplicate_check
WHERE duplicate > 0;
```

### Standardize the

