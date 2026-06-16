with source as (
    select * from {{ source('raw', 'order_items') }}
    where _fivetran_deleted = false
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_pct,
        round(unit_price * quantity * (1 - discount_pct / 100), 2) as line_total
    from source
    where order_item_id is not null
)

select * from renamed
