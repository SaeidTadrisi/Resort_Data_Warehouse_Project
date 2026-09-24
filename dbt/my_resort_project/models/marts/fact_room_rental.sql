select
    rent.rental_id,
    rent.rent_date as date_id,
    rent.person_id,
    rent.room_id,
    rent.period_days,
    room.nightly_rate,
    rent.period_days * room.nightly_rate as revenue_amount
from {{ ref("stg_rent") }} as rent
inner join {{ ref("dim_room") }} as room
    on rent.room_id = room.room_id
