select
    investment.investment_id,
    investment.investment_date as date_id,
    investment.person_id,
    investment.title_id,
    investment.investment_amount,
    investment.duration_days
from {{ ref("stg_investment") }} as investment
inner join {{ ref("dim_investment_title") }} as title
    on investment.title_id = title.title_id
