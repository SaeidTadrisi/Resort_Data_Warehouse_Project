{{ config(materialized='table') }}

SELECT DISTINCT
    Rent_Date AS DATEID,
    Rent_Date AS full_date,
    MONTH(Rent_Date) AS month,
    YEAR(Rent_Date) AS year,
    CASE
        WHEN MONTH(Rent_Date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(Rent_Date) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(Rent_Date) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Autumn'
    END AS season,
    CASE WHEN DAYOFWEEK(Rent_Date) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend,
    0 AS is_holiday,
    0 AS is_event
FROM {{ source('hotel_raw', 'Rent') }}