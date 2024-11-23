## SQL Project: Cleaning and EDA on layoff dataset

```
SELECT * FROM ;
```


### Check duplication
```sql
WITH duplicate_check as(
	SELECT
		company,
		location,
		industry,
		total_laid_off,
		percentage_laid_off,
		date,
		stage,
		country,
		funds_raised,
		ROW_NUMBER() OVER(
		PARTITION BY 	company,
						location,
						industry,
						total_laid_off,
						percentage_laid_off,
						date,
						stage,
						country,
						funds_raised
		) - 1 AS duplicate
		
	FROM layoffs_wk)
SELECT * 
FROM duplicate_check
WHERE duplicate > 0;
```

