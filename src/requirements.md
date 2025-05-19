# Technical Requirements for Incoming CSV Files

## File Naming Convention
- Expected: `ga4_public_dataset.csv`
- Files must be placed in the `platform_algorithm_bucket` in the `europe-west4` region.
- Only one file per day is expected, arriving by 7 AM CEST.

## Schema
- Columns:
  - `event_date` (STRING): Date of the event (format: YYYYMMDD, e.g., "20201220").
  - `event_timestamp` (INTEGER): Timestamp of the event in microseconds.
  - `event_name` (STRING): Name of the event (e.g., "add_shipping_info", "add_to_cart").
  - `event_params` (RECORD): Nested JSON containing event parameters (e.g., `currency`, `page_title`).
  - `event_previous_timestamp` (INTEGER): Previous event timestamp in microseconds (nullable).
  - `event_value_in_usd` (STRING): Event value in USD (nullable).
  - `event_bundle_sequence_id` (INTEGER): Sequence ID for event bundles.
  - `event_server_timestamp_offset` (INTEGER): Server timestamp offset (nullable).
  - `user_id` (INTEGER): User identifier (nullable).
  - `user_pseudo_id` (STRING): Pseudo-anonymous user identifier.
  - `privacy_info` (RECORD): Nested JSON with privacy settings (e.g., `uses_transient_token`).
  - `user_first_touch_timestamp` (INTEGER): First touch timestamp in microseconds.
  - `user_ltv` (RECORD): Nested JSON with lifetime value data (e.g., `revenue`, `currency`).
  - `device` (RECORD): Nested JSON with device info (e.g., `category`, `operating_system`).
  - `geo` (RECORD): Nested JSON with geographic info (e.g., `country`, `region`).
  - `app_info` (RECORD): Nested JSON with app info (nullable).
  - `traffic_source` (RECORD): Nested JSON with traffic source data (e.g., `medium`, `source`).
  - `stream_id` (STRING): Stream identifier (e.g., "2100450278").
  - `platform` (STRING): Platform (e.g., "WEB").
  - `event_dimensions` (RECORD): Nested JSON for event dimensions (nullable).
  - `ecommerce` (RECORD): Nested JSON with ecommerce data (e.g., `total_item_quantity`).
  - `items` (RECORD): Nested JSON array of items (e.g., `item_id`, `item_name`).
- Nested Fields (Examples):
  - `event_params`: Contains subfields like `key` (STRING) and `value` (RECORD with `string_value`, `int_value`).
  - `items`: Array of records with fields like `item_id` (STRING), `item_name` (STRING), `price` (STRING).

## Delimiters
- Comma (,)

## Constraints
- Encoding: UTF-8
- Missing Values: Handle as NULL
- Consistency: All files must adhere to the above schema