with all_dates as (

    select rent_date as full_date
    from {{ ref("stg_rent") }}

    union

    select service_date as full_date
    from {{ ref("stg_rent_service") }}

    union

    select investment_date as full_date
    from {{ ref("stg_investment") }}

)

select distinct
    full_date as date_id,
    full_date,
    day(full_date) as day_of_month,
    month(full_date) as month_number,
    monthname(full_date) as month_name,
    quarter(full_date) as quarter_number,
    year(full_date) as year_number,
    case
        when month(full_date) in (12, 1, 2) then 'Winter'
        when month(full_date) in (3, 4, 5) then 'Spring'
        when month(full_date) in (6, 7, 8) then 'Summer'
        else 'Autumn'
    end as season,
    case
        when dayofweek(full_date) in (1, 7) then true
        else false
    end as is_weekend
from all_dates
where full_date is not null

