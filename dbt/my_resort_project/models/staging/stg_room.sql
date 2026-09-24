select
    id as room_id,
    size_sqm,
    room_type,
    nightly_rate,
    hotel_id
from {{ source("hotel_raw", "room") }}
where id is not null
