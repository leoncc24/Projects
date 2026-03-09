CREATE OR REPLACE VIEW `my-project-2603-489012.ga4_google_ecom.vw_funnel` AS
WITH session_steps AS (
  SELECT
    PARSE_DATE('%Y%m%d', date) AS report_date,
    visitId,
    
    -- Session starts = every session
    MAX(1) AS session_start,
    
    -- Viewed an item
    MAX(CASE WHEN h.eCommerceAction.action_type = '2' THEN 1 ELSE 0 END) AS viewed_item,
    
    -- Added to cart
    MAX(CASE WHEN h.eCommerceAction.action_type = '3' THEN 1 ELSE 0 END) AS added_to_cart,
    
    -- Checkout started
    MAX(CASE WHEN h.eCommerceAction.action_type = '5' THEN 1 ELSE 0 END) AS checkout_started,
    
    -- Purchased
    MAX(CASE WHEN h.eCommerceAction.action_type = '6' THEN 1 ELSE 0 END) AS purchased

  FROM `my-project-2603-489012.ga4_google_ecom.ga_sessions_*`,
    UNNEST(hits) AS h
  GROUP BY report_date, visitId
)
SELECT
  report_date,
  COUNT(DISTINCT visitId) AS total_sessions,           -- Session starts
  SUM(viewed_item) AS sessions_viewed_item,
  SUM(added_to_cart) AS sessions_added_to_cart,
  SUM(checkout_started) AS sessions_checkout,
  SUM(purchased) AS sessions_purchased,
FROM session_steps
GROUP BY report_date
ORDER BY report_date DESC;

