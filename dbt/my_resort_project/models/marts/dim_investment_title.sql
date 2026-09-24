select
    title_id,
    title_type
from {{ ref("stg_stock_market_title") }}
