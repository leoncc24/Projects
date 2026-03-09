CREATE OR REPLACE VIEW `my-project-2603-489012.ga4_google_ecom.vw_daily_performance` AS
SELECT
  PARSE_DATE('%Y%m%d', date) AS report_date,
  trafficSource.medium AS medium,
  device.deviceCategory AS device_type,
  geoNetwork.country AS country,
  COUNT(*) AS sessions,
  SUM(totals.pageviews) AS pageviews,
  SAFE_DIVIDE(SUM(totals.bounces), COUNT(*)) AS bounce_rate,
  AVG(totals.timeOnSite) AS avg_session_duration_seconds,
  SUM(totals.transactions) AS transactions,
  SUM(totals.transactionRevenue) / 1000000 AS total_revenue_usd,
  SAFE_DIVIDE(SUM(totals.transactions), COUNT(*)) AS conversion_rate
FROM `my-project-2603-489012.ga4_google_ecom.ga_sessions_*`,
GROUP BY report_date, medium, device_type, country;