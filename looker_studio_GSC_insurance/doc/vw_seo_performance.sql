CREATE OR REPLACE VIEW `my-project-2603-489012.gsc.vw_seo_performance`
AS
SELECT 
  data_date,
  site_url,
  url,
  query,
  country,
  device,
  impressions,
  clicks,
  
  -- Official GSC average position (weighted)
  ROUND(SAFE_DIVIDE(SUM(sum_top_position), SUM(impressions)) + 1, 2) AS avg_position,
  
  -- Clean CTR %
  ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_percent,
  
  -- Branded vs Generic (super useful for Prudential analysis)
  CASE 
    WHEN LOWER(query) LIKE '%prudential%' 
      OR LOWER(query) LIKE '%保誠%' 
      OR LOWER(query) LIKE '%pruhealth%' 
    THEN 'Branded' 
    ELSE 'Generic' 
  END AS query_type,
  
  -- Extra helpful columns
  FORMAT_DATE('%Y-%m', data_date) AS year_month,
  EXTRACT(DAY FROM data_date) AS day_of_month

FROM `my-project-2603-489012.gsc.searchdata_url_impression`
GROUP BY 
  data_date, site_url, url, query, country, device, 
  impressions, clicks, sum_top_position;