select
    id as investment_id,
    person_id,
    title_id,
    investment_date,
    amount as investment_amount,
    duration_days
from {{ source("hotel_raw", "investment") }}
where id is not null
  and person_id is not null
  and title_id is not null
  and investment_date is not null
  and amount > 0
  and duration_days > 0
