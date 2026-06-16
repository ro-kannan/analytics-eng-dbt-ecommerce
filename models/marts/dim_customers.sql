with customers as (
    select * from {{ ref('stg_customers') }}
),

country_codes as (
    select * from {{ ref('country_codes') }}
),

final as (
    select
        c.customer_id,
        c.full_name,
        c.email,
        c.phone,
        c.country_code,
        cc.country_name,
        cc.region,
        c.created_date
    from customers c
    left join country_codes cc
        on c.country_code = cc.country_code
)

select * from final
