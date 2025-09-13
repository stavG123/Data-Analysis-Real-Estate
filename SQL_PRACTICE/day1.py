import sqlite3
import pandas as pd

# connect to your DB (make sure practice.db is in the same folder)
conn = sqlite3.connect("practice.db")
"""
Day 1 — SELECT & WHERE (ShopDB)
All USA users who signed up in 2024.
Products cheaper than 30.
Orders with status not in ('cancelled','pending').
"""
# Write your query
Q1_1 = "SELECT * FROM users " \
"WHERE signup_date LIKE '2024%' " \
"AND country = 'USA';" 

Q1_2 = "SELECT * FROM products " \
"WHERE price < 30;"


Q1_3 = "SELECT * FROM orders WHERE status NOT IN ('cancelled','pending');"

"""
Day 2 — ORDER BY & LIMIT
Top 5 most expensive products.
10 newest users by signup_date.
Latest 5 orders by order_date.

Day 3 — Aggregate Functions
Count users per country.
Avg price per category.
Total quantity sold per product_id.

day 4 — HAVING
Categories with avg price > 50.
Countries with > 2 users.
Products with total sold qty ≥ 3.

"""
# Write your query
Q2_1="SELECT * FROM products ORDER BY price DESC LIMIT 5"
Q2_2="SELECT * FROM USERS   ORDER BY signup_date DESC LIMIT 10"
Q2_3="SELECT * FROM orders ORDER BY order_date DESC LIMIT 5"
Q3_1='SELECT  country ,COUNT(*) FROM users GROUP BY country;'
Q3_2='SELECT category_id, AVG(price) AS avg_price FROM products GROUP BY category_id;'
Q3_3='SELECT product_id, SUM(quantity) AS total_quantity_sold FROM order_items GROUP BY product_id;'
Q4_1="SELECT product_id , AVG(PRICE) FROM products GROUP BY category_id HAVING AVG(PRICE) >50;"

Q4_1 = pd.read_sql(Q4_1, conn)
print(Q4_1)
conn.close()


