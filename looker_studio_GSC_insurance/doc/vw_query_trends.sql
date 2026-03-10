CREATE OR REPLACE VIEW `my-project-2603-489012.gsc.vw_query_trends`
AS
WITH daily_per_query AS (
  SELECT
    data_date,
    query,
    SUM(impressions)                          AS impressions,
    SUM(clicks)                               AS clicks,
    ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_percent,
    ROUND(SAFE_DIVIDE(SUM(sum_top_position), SUM(impressions)) + 1, 2) AS avg_position
  FROM `my-project-2603-489012.gsc.searchdata_url_impression`
  GROUP BY data_date, query
)

SELECT
  data_date,
  query,

  -- CURRENT values
  impressions                               AS impressions_current,
  clicks                                    AS clicks_current,
  ctr_percent                               AS ctr_percent_current,
  avg_position                              AS avg_position_current,

  -- PREVIOUS WEEK (7 days ago)
  LAG(impressions, 7) OVER (PARTITION BY query ORDER BY data_date) AS impressions_prev_week,
  LAG(clicks, 7)       OVER (PARTITION BY query ORDER BY data_date) AS clicks_prev_week,
  LAG(ctr_percent, 7)  OVER (PARTITION BY query ORDER BY data_date) AS ctr_percent_prev_week,
  LAG(avg_position, 7) OVER (PARTITION BY query ORDER BY data_date) AS avg_position_prev_week,

  -- WoW % CHANGE
  ROUND(
    SAFE_DIVIDE(
      impressions - LAG(impressions, 7) OVER (PARTITION BY query ORDER BY data_date),
      LAG(impressions, 7) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS wow_impressions_pct,

  ROUND(
    SAFE_DIVIDE(
      clicks - LAG(clicks, 7) OVER (PARTITION BY query ORDER BY data_date),
      LAG(clicks, 7) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS wow_clicks_pct,

  ROUND(
    SAFE_DIVIDE(
      ctr_percent - LAG(ctr_percent, 7) OVER (PARTITION BY query ORDER BY data_date),
      LAG(ctr_percent, 7) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS wow_ctr_pct,

  ROUND(
    SAFE_DIVIDE(
      avg_position - LAG(avg_position, 7) OVER (PARTITION BY query ORDER BY data_date),
      LAG(avg_position, 7) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS wow_position_pct,   -- note: positive = worse position

  -- PREVIOUS MONTH (~30 days ago)
  LAG(impressions, 30) OVER (PARTITION BY query ORDER BY data_date) AS impressions_prev_month,
  LAG(clicks, 30)       OVER (PARTITION BY query ORDER BY data_date) AS clicks_prev_month,
  LAG(ctr_percent, 30)  OVER (PARTITION BY query ORDER BY data_date) AS ctr_percent_prev_month,
  LAG(avg_position, 30) OVER (PARTITION BY query ORDER BY data_date) AS avg_position_prev_month,

  -- MoM % CHANGE
  ROUND(
    SAFE_DIVIDE(
      impressions - LAG(impressions, 30) OVER (PARTITION BY query ORDER BY data_date),
      LAG(impressions, 30) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS mom_impressions_pct,

  ROUND(
    SAFE_DIVIDE(
      clicks - LAG(clicks, 30) OVER (PARTITION BY query ORDER BY data_date),
      LAG(clicks, 30) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS mom_clicks_pct,

  ROUND(
    SAFE_DIVIDE(
      ctr_percent - LAG(ctr_percent, 30) OVER (PARTITION BY query ORDER BY data_date),
      LAG(ctr_percent, 30) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS mom_ctr_pct,

  ROUND(
    SAFE_DIVIDE(
      avg_position - LAG(avg_position, 30) OVER (PARTITION BY query ORDER BY data_date),
      LAG(avg_position, 30) OVER (PARTITION BY query ORDER BY data_date)
    ) * 100,
    1
  ) AS mom_position_pct     -- positive = worse position

FROM daily_per_query

-- Optional: only keep rows where we have enough history
WHERE data_date >= DATE_ADD((SELECT MIN(data_date) FROM daily_per_query), INTERVAL 30 DAY)

ORDER BY query, data_date;
