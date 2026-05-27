{{ config(materialized='table') }}

SELECT
    CF AS PersonID,
    CASE
        WHEN Age < 30 THEN 'Youth'
        WHEN Age BETWEEN 30 AND 50 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group,
    'Standard' AS profile_type,
    City AS city,
    Country AS country,
    'Europe/Asia' AS continent_region
FROM {{ source('hotel_raw', 'Person') }}