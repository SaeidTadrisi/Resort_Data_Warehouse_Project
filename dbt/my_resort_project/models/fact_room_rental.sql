{{ config(materialized='table') }}

SELECT
    rent.ID AS RentallD,
    rent.Rent_Date AS DateID,
    rent.Room_ID AS RoomID,
    rent.CF AS PersonID,
    rent.Period AS period_days,
    room.Price AS room_price_amount,
    (rent.Period * room.Price) AS revenue_amount
FROM {{ source('hotel_raw', 'Rent') }} rent
JOIN {{ source('hotel_raw', 'Room') }} room ON rent.Room_ID = room.ID