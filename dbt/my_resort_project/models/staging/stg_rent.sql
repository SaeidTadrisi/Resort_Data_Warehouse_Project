select
    id as rental_id,
    person_id,
    room_id,
    rent_date,
    period_days
from {{ source("hotel_raw", "rent") }}
where id is not null
  and person_id is not null
  and room_id is not null
  and rent_date is not null
  and period_days > 0
