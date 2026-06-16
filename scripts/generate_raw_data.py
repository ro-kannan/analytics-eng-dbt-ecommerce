"""
Simulates Fivetran loading raw e-commerce data into a 'raw' schema in PostgreSQL.
Generates: customers (100), products (50), orders (300), order_items (500)
Every table includes Fivetran metadata columns: _fivetran_synced, _fivetran_deleted
"""

import os
import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

# --- Connection (reads from env vars — see README "How to Run") ---
conn = psycopg2.connect(
    host=os.environ.get("PGHOST", "localhost"),
    port=int(os.environ.get("PGPORT", 5432)),
    dbname=os.environ.get("PGDATABASE", "dbt_ecommerce"),
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"]
)
cur = conn.cursor()

# --- Create raw schema ---
cur.execute("DROP SCHEMA IF EXISTS raw CASCADE;")
cur.execute("CREATE SCHEMA raw;")
print("Created raw schema")

# --- Customers (100 rows) ---
cur.execute("""
    CREATE TABLE raw.customers (
        customer_id     INTEGER PRIMARY KEY,
        first_name      VARCHAR,
        last_name       VARCHAR,
        email           VARCHAR,
        phone           VARCHAR,
        country_code    VARCHAR,
        created_at      TIMESTAMP,
        _fivetran_synced    TIMESTAMP,
        _fivetran_deleted   BOOLEAN
    );
""")

countries = ['IN', 'US', 'UAE', 'SG', 'GB', 'AU', 'DE', 'CA']
country_weights = [50, 20, 8, 8, 5, 4, 3, 2]

customers = []
for i in range(1, 101):
    created = fake.date_time_between(start_date='-2y', end_date='-3m')
    customers.append((
        i,
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number()[:15],
        random.choices(countries, weights=country_weights)[0],
        created,
        datetime.now(),
        False
    ))

cur.executemany("""
    INSERT INTO raw.customers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", customers)
print(f"Inserted {len(customers)} customers")

# --- Products (50 rows) ---
cur.execute("""
    CREATE TABLE raw.products (
        product_id      INTEGER PRIMARY KEY,
        product_name    VARCHAR,
        category        VARCHAR,
        sub_category    VARCHAR,
        price           NUMERIC(10,2),
        cost_price      NUMERIC(10,2),
        sku             VARCHAR,
        is_active       BOOLEAN,
        created_at      TIMESTAMP,
        _fivetran_synced    TIMESTAMP,
        _fivetran_deleted   BOOLEAN
    );
""")

product_catalog = [
    ("Wireless Headphones", "Electronics", "Audio", 2999, 1500),
    ("Bluetooth Speaker", "Electronics", "Audio", 3500, 1800),
    ("Laptop Stand", "Electronics", "Accessories", 1800, 800),
    ("USB-C Hub", "Electronics", "Accessories", 2200, 1000),
    ("Mechanical Keyboard", "Electronics", "Peripherals", 4500, 2200),
    ("Wireless Mouse", "Electronics", "Peripherals", 1500, 700),
    ("Running Shoes", "Footwear", "Sports", 4500, 2000),
    ("Casual Sneakers", "Footwear", "Casual", 3200, 1400),
    ("Formal Shoes", "Footwear", "Formal", 3800, 1600),
    ("Sandals", "Footwear", "Casual", 1200, 500),
    ("Cotton T-Shirt", "Apparel", "Tops", 599, 250),
    ("Polo T-Shirt", "Apparel", "Tops", 899, 350),
    ("Denim Jeans", "Apparel", "Bottoms", 1999, 900),
    ("Chino Pants", "Apparel", "Bottoms", 1799, 800),
    ("Hoodie", "Apparel", "Outerwear", 1499, 650),
    ("Jacket", "Apparel", "Outerwear", 2999, 1300),
    ("Yoga Mat", "Fitness", "Equipment", 1200, 500),
    ("Resistance Bands", "Fitness", "Equipment", 699, 300),
    ("Dumbbells Set", "Fitness", "Equipment", 3500, 1500),
    ("Water Bottle", "Fitness", "Accessories", 450, 180),
    ("Protein Shaker", "Fitness", "Accessories", 350, 150),
    ("Backpack", "Accessories", "Bags", 2200, 950),
    ("Laptop Bag", "Accessories", "Bags", 2800, 1200),
    ("Wallet", "Accessories", "Leather", 899, 380),
    ("Belt", "Accessories", "Leather", 699, 300),
    ("Sunglasses", "Accessories", "Eyewear", 1500, 650),
    ("Face Wash", "Beauty", "Skincare", 299, 120),
    ("Moisturizer", "Beauty", "Skincare", 499, 200),
    ("Shampoo", "Beauty", "Haircare", 349, 140),
    ("Conditioner", "Beauty", "Haircare", 349, 140),
    ("Notebook Set", "Stationery", "Writing", 299, 120),
    ("Pen Set", "Stationery", "Writing", 199, 80),
    ("Desk Organizer", "Stationery", "Office", 599, 250),
    ("Sticky Notes", "Stationery", "Office", 149, 60),
    ("Phone Case", "Electronics", "Accessories", 499, 200),
    ("Screen Protector", "Electronics", "Accessories", 299, 120),
    ("Charging Cable", "Electronics", "Accessories", 399, 160),
    ("Power Bank", "Electronics", "Power", 2499, 1100),
    ("Smart Watch", "Electronics", "Wearables", 8999, 4000),
    ("Fitness Band", "Electronics", "Wearables", 3999, 1800),
    ("Coffee Mug", "Kitchen", "Drinkware", 399, 160),
    ("Thermos", "Kitchen", "Drinkware", 899, 380),
    ("Lunch Box", "Kitchen", "Storage", 699, 290),
    ("Cutting Board", "Kitchen", "Utensils", 499, 200),
    ("Knife Set", "Kitchen", "Utensils", 1299, 560),
    ("Candle", "Home", "Decor", 499, 200),
    ("Photo Frame", "Home", "Decor", 399, 160),
    ("Cushion Cover", "Home", "Textiles", 299, 120),
    ("Bedsheet Set", "Home", "Textiles", 1499, 650),
    ("Towel Set", "Home", "Textiles", 799, 340),
]

products = []
for i, (name, cat, sub_cat, price, cost) in enumerate(product_catalog, 1):
    products.append((
        i, name, cat, sub_cat,
        price, cost,
        f"SKU-{i:04d}",
        True,
        fake.date_time_between(start_date='-2y', end_date='-1y'),
        datetime.now(),
        False
    ))

cur.executemany("""
    INSERT INTO raw.products VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", products)
print(f"Inserted {len(products)} products")

# --- Orders (300 rows) ---
cur.execute("""
    CREATE TABLE raw.orders (
        order_id        INTEGER PRIMARY KEY,
        customer_id     INTEGER,
        order_date      TIMESTAMP,
        status          VARCHAR,
        payment_method  VARCHAR,
        shipping_address VARCHAR,
        country_code    VARCHAR,
        _fivetran_synced    TIMESTAMP,
        _fivetran_deleted   BOOLEAN
    );
""")

statuses = ['completed', 'shipped', 'returned', 'cancelled', 'pending']
status_weights = [65, 15, 8, 8, 4]
payment_methods = ['credit_card', 'debit_card', 'upi', 'net_banking', 'wallet']
payment_weights = [30, 25, 30, 10, 5]

orders = []
for i in range(1, 301):
    customer = random.choice(customers)
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    orders.append((
        i,
        customer[0],
        order_date,
        random.choices(statuses, weights=status_weights)[0],
        random.choices(payment_methods, weights=payment_weights)[0],
        fake.address()[:100],
        customer[5],
        datetime.now(),
        False
    ))

cur.executemany("""
    INSERT INTO raw.orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", orders)
print(f"Inserted {len(orders)} orders")

# --- Order Items (500 rows) ---
cur.execute("""
    CREATE TABLE raw.order_items (
        order_item_id   INTEGER PRIMARY KEY,
        order_id        INTEGER,
        product_id      INTEGER,
        quantity        INTEGER,
        unit_price      NUMERIC(10,2),
        discount_pct    NUMERIC(5,2),
        _fivetran_synced    TIMESTAMP,
        _fivetran_deleted   BOOLEAN
    );
""")

order_items = []
item_id = 1
order_ids_used = random.sample(range(1, 301), 280)

for order_id in order_ids_used:
    num_items = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
    product_ids_in_order = random.sample(range(1, 51), min(num_items, 50))
    for product_id in product_ids_in_order:
        product = products[product_id - 1]
        unit_price = product[4]
        discount = random.choices([0, 5, 10, 15, 20], weights=[50, 20, 15, 10, 5])[0]
        order_items.append((
            item_id,
            order_id,
            product_id,
            random.randint(1, 4),
            unit_price,
            discount,
            datetime.now(),
            False
        ))
        item_id += 1
        if item_id > 501:
            break
    if item_id > 501:
        break

cur.executemany("""
    INSERT INTO raw.order_items VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""", order_items)
print(f"Inserted {len(order_items)} order items")

conn.commit()
cur.close()
conn.close()
print("\nDone! Raw schema loaded successfully.")
