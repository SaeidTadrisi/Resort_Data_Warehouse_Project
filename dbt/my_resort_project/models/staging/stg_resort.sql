select
    id as resort_id,
    name as resort_name,
    city as resort_city,
    country as resort_country
from {{ source("hotel_raw", "resort") }}
where id is not null
