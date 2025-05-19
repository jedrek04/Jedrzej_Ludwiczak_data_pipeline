SELECT
  JSON_EXTRACT_SCALAR(JSON_EXTRACT(geo, '$.geo'), '$.country') AS country,
  COUNT(*) AS add_to_cart_event_count
FROM
  `crystalloids-candidates.platform_assignment_dataset.Jedrzej_Ludwiczak_ga4_table`
WHERE
  event_name = 'add_to_cart'
  AND JSON_EXTRACT_SCALAR(JSON_EXTRACT(geo, '$.geo'), '$.country') IS NOT NULL
GROUP BY
  country
ORDER BY
  add_to_cart_event_count DESC