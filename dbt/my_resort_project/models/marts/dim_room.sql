select
    room.room_id,
    room.room_type,
    room.size_sqm,
    room.nightly_rate,
    hotel.hotel_id,
    hotel.hotel_name,
    hotel.hotel_city,
    hotel.hotel_country,
    resort.resort_id,
    resort.resort_name,
    resort.resort_city,
    resort.resort_country
from {{ ref("stg_room") }} as room
inner join {{ ref("stg_hotel") }} as hotel
    on room.hotel_id = hotel.hotel_id
inner join {{ ref("stg_resort") }} as resort
    on hotel.resort_id = resort.resort_id
