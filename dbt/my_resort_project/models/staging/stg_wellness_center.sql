select
    id as wellness_center_id,
    name as wellness_center_name,
    city as wellness_center_city,
    country as wellness_center_country,
    resort_id
from {{ source("hotel_raw", "wellness_center") }}
where id is not null
