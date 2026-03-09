CREATE OR REPLACE VIEW `your-project.ga4_google_ecom.vw_popular_pages` AS
WITH page_level AS (
  SELECT
    PARSE_DATE('%Y%m%d', date) AS report_date,
    h.page.pagePath AS page_path,
    trafficSource.source AS session_source,
    trafficSource.medium AS session_medium,
    
    -- Core metrics
    COUNT(*) AS pageviews,
    SUM(CASE WHEN h.isEntrance = TRUE THEN 1 ELSE 0 END) AS entrances,
    AVG(h.time / 1000) AS avg_time_on_page_seconds,
    
    -- For bounce rate calculation
    visitId,
    totals.pageviews AS session_total_pageviews
    
  FROM `your-project.ga4_google_ecom.ga_sessions_*`,
    UNNEST(hits) AS h
  WHERE h.type = 'PAGE'
  GROUP BY 
    report_date, page_path, session_source, session_medium,
    visitId, session_total_pageviews
),

aggregated AS (
  SELECT
    report_date,
    page_path,
    session_source,
    session_medium,
    
    COUNT(*) AS pageviews,
    SUM(entrances) AS entrances,
    AVG(avg_time_on_page_seconds) AS avg_time_on_page_seconds,
    
    -- Bounce rate approximation:
    -- Sessions that entered on this page AND had only 1 pageview in the whole session
    SUM(CASE WHEN entrances > 0 AND session_total_pageviews = 1 THEN 1 ELSE 0 END) AS bounced_sessions,
    COUNT(DISTINCT visitId) AS total_sessions_with_this_page,
    
    SAFE_DIVIDE(
      SUM(CASE WHEN entrances > 0 AND session_total_pageviews = 1 THEN 1 ELSE 0 END),
      SUM(CASE WHEN entrances > 0 THEN 1 ELSE 0 END)
    ) * 100 AS entrance_page_bounce_rate_pct

  FROM page_level
  GROUP BY 
    report_date, page_path, session_source, session_medium
)

SELECT *
FROM aggregated
WHERE entrances > 0  -- only pages that were actually landed on
ORDER BY report_date DESC, entrances DESC;
