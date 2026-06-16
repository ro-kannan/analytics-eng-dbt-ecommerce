{{ config(
    materialized='incremental',
    unique_key='order_id',
    post_hook="
        delete from {{ this }}
        where order_id not in (select order_id from {{ ref('stg_orders') }})
    "
) }}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
    where synced_at > (select max(synced_at) from {{ this }})
    {% endif %}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_statuses as (
    select * from {{ ref('order_statuses') }}
),

order_totals as (
    select
        order_id,
        sum(line_total)   as order_total,
        sum(quantity)     as total_items
    from order_items
    group by order_id
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        os.status_label,
        os.is_revenue,
        o.payment_method,
        o.country_code,
        o.synced_at,
        coalesce(ot.total_items, 0)  as total_items,
        case
            when os.is_revenue = true then coalesce(ot.order_total, 0)
            else 0
        end                          as revenue
    from orders o
    left join order_totals ot
        on o.order_id = ot.order_id
    left join order_statuses os
        on o.status = os.status_code
)

select * from final
