with orders as (
    select * from {{ ref('fct_orders') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
),

order_summary as (
    select
        customer_id,
        count(order_id)                                    as total_orders,
        sum(revenue)                                       as total_revenue,
        min(order_date)                                    as first_order_date,
        max(order_date)                                    as last_order_date,
        count(case when status = 'returned' then 1 end)   as total_returns,
        count(case when status = 'completed' then 1 end)  as completed_orders
    from orders
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.full_name,
        c.email,
        c.country_name,
        c.region,
        c.created_date                                      as customer_since,
        coalesce(os.total_orders, 0)                        as total_orders,
        coalesce(os.completed_orders, 0)                    as completed_orders,
        coalesce(os.total_returns, 0)                       as total_returns,
        coalesce(os.total_revenue, 0)                       as total_revenue,
        os.first_order_date,
        os.last_order_date
    from customers c
    left join order_summary os
        on c.customer_id = os.customer_id
)

select * from final
