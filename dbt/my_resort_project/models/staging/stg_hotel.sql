select
    id as hotel_id,
    name as hotel_name,
    city as hotel_city,
    country as hotel_country,
    resort_id
from {{ source("hotel_raw", "hotel") }}
where id is not null
