select
    person_id,
    full_name,
    gender,
    city,
    country,
    case
        when age < 30 then 'Youth'
        when age between 30 and 50 then 'Adult'
        else 'Senior'
    end as age_group
from {{ ref("stg_person") }}

