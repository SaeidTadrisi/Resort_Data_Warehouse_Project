select
    id as person_id,
    full_name,
    age,
    gender,
    city,
    country
from {{ source("hotel_raw", "person") }}
where id is not null
