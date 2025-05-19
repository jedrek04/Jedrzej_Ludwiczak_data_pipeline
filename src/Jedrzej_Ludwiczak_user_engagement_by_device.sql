SELECT
  JSON_EXTRACT_SCALAR(JSON_EXTRACT(device, '$.device'), '$.category') AS device_category,
  COUNT(*) AS view_item_event_count
FROM
  `crystalloids-candidates.platform_assignment_dataset.Jedrzej_Ludwiczak_ga4_table`
WHERE
  event_name = 'view_item'
  AND JSON_EXTRACT_SCALAR(JSON_EXTRACT(device, '$.device'), '$.category') IS NOT NULL
GROUP BY
  device_category
ORDER BY
  view_item_event_count DESC