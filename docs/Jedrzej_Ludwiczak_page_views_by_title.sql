SELECT
  JSON_EXTRACT_SCALAR(param, '$.value.string_value') AS page_title,
  COUNT(*) AS total_views
FROM
  `crystalloids-candidates.platform_assignment_dataset.Jedrzej_Ludwiczak_ga4_table`,
  UNNEST(JSON_EXTRACT_ARRAY(event_params, '$.event_params')) AS param
WHERE
  event_name = 'view_item'
  AND JSON_EXTRACT_SCALAR(param, '$.key') = 'page_title'
  AND JSON_EXTRACT_SCALAR(param, '$.value.string_value') IS NOT NULL
GROUP BY
  page_title
ORDER BY
  total_views DESC