select
    id as service_id,
    service_type,
    duration_minutes,
    price as service_price,
    wellness_center_id
from {{ source("hotel_raw", "specific_service") }}
where id is not null
