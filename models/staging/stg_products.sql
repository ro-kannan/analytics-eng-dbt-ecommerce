with source as (
    select * from {{ source('raw', 'products') }}
    where _fivetran_deleted = false
),

renamed as (
    select
        product_id,
        lower(product_name)    as product_name,
        lower(category)        as category,
        lower(sub_category)    as sub_category,
        price,
        cost_price,
        sku,
        is_active,
        created_at::date       as created_date
    from source
    where product_id is not null
)

select * from renamed
