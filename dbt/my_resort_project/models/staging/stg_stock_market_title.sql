select
    id as title_id,
    title_type
from {{ source("hotel_raw", "stock_market_title") }}
where id is not null
