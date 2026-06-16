with source as (
    select * from {{ source('raw', 'orders') }}
    where _fivetran_deleted = false
),

renamed as (
    select
        order_id,
        customer_id,
        order_date::date           as order_date,
        lower(status)              as status,
        lower(payment_method)      as payment_method,
        country_code,
        _fivetran_synced           as synced_at
    from source
    where order_id is not null
)

select * from renamed
