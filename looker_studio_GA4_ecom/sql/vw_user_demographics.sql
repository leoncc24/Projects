CREATE OR REPLACE VIEW `my-project-2603-489012.ga4_google_ecom.vw_user_demographics` AS
SELECT
  PARSE_DATE('%Y%m%d', date) AS report_date,
  
  -- Device & OS
  device.deviceCategory AS device_type,
  device.operatingSystem AS operating_system,
  device.operatingSystemVersion AS os_version,
  
  -- Browser
  device.browser AS browser,
  device.browserVersion AS browser_version,
  
  -- Geo
  geoNetwork.continent AS continent,
  geoNetwork.country AS country,
  geoNetwork.region AS region,
  
  -- Metrics
  COUNT(*) AS sessions,
  COUNT(DISTINCT fullVisitorId) AS users,
  SUM(CASE WHEN totals.newVisits = 1 THEN 1 ELSE 0 END) AS new_users,
  SUM(totals.pageviews) AS pageviews,
  SAFE_DIVIDE(SUM(totals.bounces), COUNT(*)) AS bounce_rate,
  
  -- Calculated percentages
  SAFE_DIVIDE(
    SUM(CASE WHEN totals.newVisits = 1 THEN 1 ELSE 0 END), 
    COUNT(*)
  ) AS new_user_percentage

FROM `my-project-2603-489012.ga4_google_ecom.ga_sessions_*`
GROUP BY 
  report_date,
  device_type,
  operating_system,
  os_version,
  browser,
  browser_version,
  continent,
  country,
  region;
