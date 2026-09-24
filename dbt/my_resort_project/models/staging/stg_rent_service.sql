select
    id as service_usage_id,
    person_id,
    service_id,
    service_date
from {{ source("hotel_raw", "rent_service") }}
where id is not null
  and person_id is not null
  and service_id is not null
  and service_date is not null
