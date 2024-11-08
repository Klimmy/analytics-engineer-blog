{{ config(materialized="table") }}

WITH data AS (
  SELECT
    trafficSource.source AS traffic_source,
    SUM(totals.visits) AS visits,
    COALESCE(SUM(totals.transactions), 0) AS conversions,
    (COALESCE(SUM(totals.transactions), 0) / SUM(totals.visits)) AS CVR
  FROM {{ source('ga4_public_data', 'ga_sessions') }}
  GROUP BY trafficSource.source
)

SELECT
  traffic_source AS `Traffic Source`,
  visits AS Visits,
  conversions AS Conversions,
  ROUND(CVR * 100, 2) AS CVR,
  ROUND(({{ wilson_lower_bound('CVR', 'visits') }}) * 100, 2) AS `CVR Lower CI`,
  ROUND(((0.4 + conversions) / (0.4 + conversions + 42.6 + visits)) * 100, 2) AS `CVR Beta`
FROM data
ORDER BY `CVR Beta` DESC
