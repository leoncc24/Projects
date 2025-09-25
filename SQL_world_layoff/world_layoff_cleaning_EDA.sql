-- Data Cleaning

-- 1. Remove duplicates
-- Copy raw data from layoffs into layoffs_staging
CREATE TABLE layoffs_staging
LIKE layoffs;

INSERT layoffs_staging
SELECT *
FROM layoffs;

SELECT*,
ROW_NUMBER() OVER(PARTITION BY company, industry, total_laid_off, percentage_laid_off,  'date') AS row_num
FROM layoffs_staging;

-- Use row number to check any >1 which mean their columns are the same
WITH duplicate_cte AS
(
SELECT*,
ROW_NUMBER() OVER(PARTITION BY company, industry, location, stage, country, funds_raised_millions, total_laid_off, percentage_laid_off,  'date') AS row_num
FROM layoffs_staging
)
SELECT *
FROM duplicate_cte
WHERE row_num >1;

-- Right click the table layoffs_staging and click Copy to clipboard- Create statement
-- Make a copy of layoffs_staging2 which exclude the row number >1
CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Copy all data from layoffs_staging into layoffs_staging2
INSERT INTO layoffs_staging2
SELECT*,
ROW_NUMBER() OVER(PARTITION BY company, industry, location, stage, country, funds_raised_millions, total_laid_off, percentage_laid_off,  'date') AS row_num
FROM layoffs_staging ;

-- Delete row number >1 in layoffs_staging2
DELETE
FROM layoffs_staging2
WHERE row_num >1;


-- 2. Standardize the Data
-- Trim company name
UPDATE layoffs_staging2
SET company = TRIM(company);

-- Check industry categories, then we will see Crypto, Crypto Currency and CryptoCurrency which should be grouped as one category
SELECT  DISTINCT industry
FROM layoffs_staging2
ORDER BY 1;

-- Change all Crypto like into Crypto
UPDATE layoffs_staging2
SET industry = 'Crypto'
WHERE industry LIKE 'Crypto%';

-- In country column, we have United States and United States.
SELECT  DISTINCT country
FROM layoffs_staging2
ORDER BY 1;

-- Change all United States like into United States
UPDATE layoffs_staging2
SET country = 'United States'
WHERE country LIKE 'United States%';

-- Format the date column
UPDATE layoffs_staging2
SET `date` = STR_TO_DATE(`date`, '%m/%d/%Y');

ALTER TABLE layoffs_staging2
MODIFY COLUMN `date` DATE;


-- 3. Null values or blank values
-- Check the company whose industry column is null or empty, there are four companies
SELECT *
FROM layoffs_staging2
WHERE industry IS NULL
OR industry = '';

-- Update the empty into Null
UPDATE layoffs_staging2
Set industry = Null
WHERE industry = '';

-- Try fill the Null industries with the industries provided in the other rows with same company name
UPDATE layoffs_staging2 t1
JOIN layoffs_staging2 t2
	ON t1.company = t2.company
    AND t1.location = t2.location
SET t1.industry = t2.industry
WHERE t1.industry IS NULL 
AND t2.industry IS NOT NULL;

-- Delete row which both total_laid_off and percentage_laid_off columns is null
DELETE
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

-- 4. Romve any columns
ALTER TABLE layoffs_staging2
DROP COLUMN row_num;

SELECT *
FROM layoffs_staging2;

-- Exploratory Data Analysis
-- Briefly check comapny with 100% layoff
SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off =1
ORDER BY total_laid_off DESC;

-- Check company with most laid off
SELECT company, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company
ORDER BY 2 DESC;

-- Check the data period, the time range covered by the dataset to know more about the background of the data
SELECT MIN(`date`), MAX(`date`)
FROM layoffs_staging2;

-- Check the most impacted industries during this period
SELECT industry, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY industry
ORDER BY 2 DESC;

-- Check the most impacted countries during this period
SELECT country, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY country
ORDER BY 2 DESC;

-- Check the most impacted year and also the trend of the impact during this period
SELECT YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY YEAR(`date`)
ORDER BY 1 DESC;

-- Check monthly laid off and the rolling total trend 
WITH cte AS(
SELECT DATE_FORMAT(`date`,'%Y-%m') AS `year_month`, SUM(total_laid_off) AS sub_total
FROM layoffs_staging2
WHERE DATE_FORMAT(`date`,'%Y-%m') IS NOT NULL
GROUP BY `year_month`
)
SELECT `year_month`,sub_total, SUM(sub_total)OVER(ORDER BY `year_month`) as rolling_total
FROM cte;
 
 -- Check the top 5 laid off company each year
 WITH cte AS(
 SELECT company, `year`, year_sum, DENSE_RANK()OVER(PARTITION BY `year` ORDER BY year_sum DESC) AS RANKING
 FROM
 (SELECT company, YEAR(`date`) AS `year`, SUM(total_laid_off) AS year_sum
 FROM layoffs_staging2
 GROUP BY company, YEAR(`date`)
 ) subquery
 )
 SELECT *
 FROM cte
 WHERE RANKING <= 5;
 
 