CREATE OR REPLACE VIEW `my-project-2603-489012.ga4_google_ecom.vw_popular_sku` AS
SELECT
  PARSE_DATE('%Y%m%d', date) AS report_date,
  p.productSku AS sku,
  p.v2ProductName AS product_name,
  p.productCategory AS category,
  SUM(p.productQuantity) AS units_sold,
  SUM(p.productRevenue) / 1000000 AS revenue_usd
FROM `my-project-2603-489012.ga4_google_ecom.ga_sessions_*`,
  UNNEST(hits) AS h,
  UNNEST(h.product) AS p
WHERE p.productSku IS NOT NULL
GROUP BY report_date, sku, product_name, category
ORDER BY revenue_usd DESC;
