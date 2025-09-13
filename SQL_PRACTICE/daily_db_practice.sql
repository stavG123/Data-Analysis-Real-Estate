
-- =============================================
-- Daily DB Practice Starter: SQLite-compatible
-- Load with: sqlite3 practice.db < daily_db_practice.sql
-- =============================================

PRAGMA foreign_keys = ON;

-- =====================
-- SHOPDB SCHEMA
-- =====================
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  country TEXT,
  signup_date TEXT
);

CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY,
  category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  price REAL NOT NULL CHECK (price >= 0),
  created_at TEXT,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE inventory (
  product_id INTEGER PRIMARY KEY,
  stock_qty INTEGER NOT NULL CHECK (stock_qty >= 0),
  reorder_level INTEGER NOT NULL DEFAULT 10,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','paid','shipped','delivered','cancelled')),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price REAL NOT NULL CHECK (unit_price >= 0),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
  payment_id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL UNIQUE,
  amount REAL NOT NULL CHECK (amount >= 0),
  method TEXT CHECK (method IN ('card','paypal','bank','giftcard')),
  paid_at TEXT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE shipments (
  shipment_id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL UNIQUE,
  shipped_at TEXT,
  delivered_at TEXT,
  carrier TEXT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE reviews (
  review_id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  created_at TEXT,
  UNIQUE(product_id, user_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Seed data: users
INSERT INTO users (user_id, name, email, country, signup_date) VALUES
(1,'Alice Johnson','alice@example.com','USA','2024-01-15'),
(2,'Bob Smith','bob@example.com','USA','2024-02-01'),
(3,'Carlos Diaz','carlos@example.com','Mexico','2024-02-12'),
(4,'Dina Levi','dina@example.com','Israel','2024-03-05'),
(5,'Ethan Wong','ethan@example.com','Canada','2024-03-10'),
(6,'Fatima Khan','fatima@example.com','UAE','2024-04-01'),
(7,'Grace Lee','grace@example.com','USA','2024-04-15'),
(8,'Hiro Tanaka','hiro@example.com','Japan','2024-05-01'),
(9,'Ivy Chen','ivy@example.com','USA','2024-05-07'),
(10,'Jonas Berg','jonas@example.com','Sweden','2024-05-21');

-- Seed data: categories
INSERT INTO categories (category_id, category_name) VALUES
(1,'Electronics'),
(2,'Books'),
(3,'Home'),
(4,'Sports'),
(5,'Beauty');

-- Seed data: products
INSERT INTO products (product_id, product_name, category_id, price, created_at) VALUES
(1,'Wireless Mouse',1,24.99,'2024-01-10'),
(2,'Mechanical Keyboard',1,89.90,'2024-01-25'),
(3,'USB-C Cable',1,9.50,'2024-02-05'),
(4,'Data Science Book',2,39.00,'2024-02-20'),
(5,'Cooking Essentials',3,59.00,'2024-03-01'),
(6,'Yoga Mat',4,29.99,'2024-03-10'),
(7,'Dumbbell Set',4,79.99,'2024-03-20'),
(8,'Face Serum',5,25.00,'2024-04-05'),
(9,'Air Purifier',3,149.00,'2024-04-10'),
(10,'Noise Cancelling Headphones',1,199.00,'2024-04-20');

-- Seed data: inventory
INSERT INTO inventory (product_id, stock_qty, reorder_level) VALUES
(1,120,20),(2,60,10),(3,500,100),(4,80,15),(5,45,10),
(6,150,30),(7,35,10),(8,200,50),(9,25,10),(10,18,8);

-- Seed data: orders
INSERT INTO orders (order_id, user_id, order_date, status) VALUES
(1001,1,'2024-04-01','paid'),
(1002,2,'2024-04-02','paid'),
(1003,3,'2024-04-03','shipped'),
(1004,1,'2024-04-10','delivered'),
(1005,4,'2024-04-11','cancelled'),
(1006,5,'2024-04-15','pending'),
(1007,6,'2024-04-18','paid'),
(1008,7,'2024-04-22','delivered'),
(1009,8,'2024-04-25','shipped'),
(1010,9,'2024-05-01','paid');

-- Seed data: order_items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1,1001,1,2,24.99),
(2,1001,3,1,9.50),
(3,1002,2,1,89.90),
(4,1003,6,1,29.99),
(5,1003,7,1,79.99),
(6,1004,10,1,199.00),
(7,1005,5,1,59.00),
(8,1006,4,1,39.00),
(9,1007,8,3,25.00),
(10,1008,9,1,149.00),
(11,1009,3,5,9.50),
(12,1010,1,1,24.99),
(13,1010,2,1,89.90);

-- Seed data: payments
INSERT INTO payments (payment_id, order_id, amount, method, paid_at) VALUES
(5001,1001,59.48,'card','2024-04-01 10:00:00'),
(5002,1002,89.90,'paypal','2024-04-02 09:12:00'),
(5003,1003,109.98,'card','2024-04-03 11:30:00'),
(5004,1004,199.00,'bank','2024-04-10 13:44:00'),
(5007,1007,75.00,'card','2024-04-18 15:05:00'),
(5010,1010,114.89,'giftcard','2024-05-01 12:00:00');

-- Seed data: shipments
INSERT INTO shipments (shipment_id, order_id, shipped_at, delivered_at, carrier) VALUES
(7003,1003,'2024-04-04 10:00:00',NULL,'DHL'),
(7004,1004,'2024-04-11 08:00:00','2024-04-13 17:22:00','UPS'),
(7008,1008,'2024-04-23 09:30:00','2024-04-25 18:10:00','USPS'),
(7009,1009,'2024-04-26 14:15:00',NULL,'FedEx');

-- Seed data: reviews
INSERT INTO reviews (review_id, product_id, user_id, rating, comment, created_at) VALUES
(9001,1,1,5,'Great mouse!','2024-04-05'),
(9002,2,2,4,'Nice keyboard','2024-04-06'),
(9003,6,3,5,'Yoga mat is comfy','2024-04-08'),
(9004,10,1,3,'Good sound but pricey','2024-04-15'),
(9005,9,7,4,'Air feels cleaner','2024-04-26'),
(9006,8,6,5,'Serum works well','2024-04-19');

-- Helper VIEW: order totals
DROP VIEW IF EXISTS v_order_totals;
CREATE VIEW v_order_totals AS
SELECT oi.order_id,
       SUM(oi.quantity * oi.unit_price) AS subtotal,
       COUNT(*) AS line_count
FROM order_items oi
GROUP BY oi.order_id;

-- =====================
-- HRDB SCHEMA
-- =====================
DROP TABLE IF EXISTS salaries;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
  dept_id INTEGER PRIMARY KEY,
  dept_name TEXT UNIQUE NOT NULL
);

CREATE TABLE employees (
  emp_id INTEGER PRIMARY KEY,
  full_name TEXT NOT NULL,
  dept_id INTEGER NOT NULL,
  hire_date TEXT NOT NULL,
  salary REAL NOT NULL CHECK (salary >= 0),
  manager_id INTEGER,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
  FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);

CREATE TABLE salaries (
  sal_id INTEGER PRIMARY KEY,
  emp_id INTEGER NOT NULL,
  effective_date TEXT NOT NULL,
  base REAL NOT NULL,
  bonus REAL NOT NULL DEFAULT 0,
  FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

INSERT INTO departments (dept_id, dept_name) VALUES
(1,'Engineering'),(2,'Sales'),(3,'HR'),(4,'Finance');

INSERT INTO employees (emp_id, full_name, dept_id, hire_date, salary, manager_id) VALUES
(1,'Nina Patel',1,'2023-01-05',120000,NULL),
(2,'Omar Ali',1,'2023-03-12',95000,1),
(3,'Priya Gupta',2,'2023-02-18',80000,NULL),
(4,'Quentin Marsh',2,'2024-01-20',70000,3),
(5,'Rina Cohen',3,'2023-05-30',65000,NULL),
(6,'Samir Aziz',4,'2023-07-14',90000,NULL),
(7,'Tara Young',1,'2024-02-01',88000,1),
(8,'Uriel Levi',4,'2024-03-03',75000,6),
(9,'Vera Zhou',2,'2024-03-17',72000,3),
(10,'Wei Chen',1,'2024-04-10',85000,1);

INSERT INTO salaries (sal_id, emp_id, effective_date, base, bonus) VALUES
(1,1,'2024-01-01',125000,15000),
(2,2,'2024-01-01',99000,5000),
(3,3,'2024-01-01',82000,8000),
(4,4,'2024-01-01',73000,3000),
(5,5,'2024-01-01',67000,2000),
(6,6,'2024-01-01',92000,12000),
(7,7,'2024-01-01',90000,5000),
(8,8,'2024-01-01',77000,4000),
(9,9,'2024-01-01',74000,3500),
(10,10,'2024-01-01',88000,6000);

-- Example indexes (SQLite auto-creates for PKs/UNIQUEs; here are extras)
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_employees_dept ON employees(dept_id);

-- Example trigger: prevent negative inventory on insert/update of order_items
DROP TRIGGER IF EXISTS trg_decrement_inventory;
CREATE TRIGGER trg_decrement_inventory
AFTER INSERT ON order_items
BEGIN
  UPDATE inventory
    SET stock_qty = stock_qty - NEW.quantity
    WHERE product_id = NEW.product_id;

  -- If stock goes negative, raise an error
  SELECT
    CASE
      WHEN (SELECT stock_qty FROM inventory WHERE product_id = NEW.product_id) < 0
      THEN RAISE(ABORT, 'Insufficient stock for this product')
    END;
END;

-- Example view: monthly revenue
DROP VIEW IF EXISTS v_monthly_revenue;
CREATE VIEW v_monthly_revenue AS
SELECT substr(p.paid_at,1,7) AS yyyy_mm,
       SUM(p.amount) AS revenue
FROM payments p
GROUP BY substr(p.paid_at,1,7);

-- Ready!
