with source as (
    select * from {{ source('raw', 'customers') }}
    where _fivetran_deleted = false
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name  as full_name,
        lower(email)                     as email,
        phone,
        country_code,
        created_at::date                 as created_date
    from source
    where email is not null
)

select * from renamed
