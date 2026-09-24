select
    service_usage.service_usage_id,
    service_usage.service_date as date_id,
    service_usage.person_id,
    service_usage.service_id,
    service.service_price,
    service.service_price as revenue_amount
from {{ ref("stg_rent_service") }} as service_usage
inner join {{ ref("dim_service") }} as service
    on service_usage.service_id = service.service_id
