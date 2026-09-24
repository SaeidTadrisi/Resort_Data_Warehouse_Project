select
    service.service_id,
    service.service_type,
    service.duration_minutes,
    service.service_price,
    wellness_center.wellness_center_id,
    wellness_center.wellness_center_name,
    wellness_center.wellness_center_city,
    wellness_center.wellness_center_country,
    resort.resort_id,
    resort.resort_name
from {{ ref("stg_specific_service") }} as service
inner join {{ ref("stg_wellness_center") }} as wellness_center
    on service.wellness_center_id = wellness_center.wellness_center_id
inner join {{ ref("stg_resort") }} as resort
    on wellness_center.resort_id = resort.resort_id
