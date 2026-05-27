{{ config(materialized='table') }}

SELECT
    r.ID AS RoomID,
    r.Type AS room_type,
    r.Size AS room_size,
    h.City AS hotel_city,
    h.Country AS hotel_country,
    'Global' AS hotel_continent
FROM {{ source('hotel_raw', 'Room') }} r
JOIN {{ source('hotel_raw', 'Hotel') }} h ON r.Hotel_ID = h.ID