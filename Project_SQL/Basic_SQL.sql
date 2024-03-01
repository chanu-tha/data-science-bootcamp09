--TABLE_1 customers' information
CREATE TABLE customers(
  id INT unique,
  name VARCHAR(30),
  lastname VARCHAR(30),
  age INT,
  gender VARCHAR(6),
  member BOOLEAN
);

--TABLE_2 Menu
CREATE TABLE menu(
  menu_id INT unique,
  name VARCHAR(30),
  price REAL
);

--TABLE_3 Order
CREATE TABLE orders(
  order_id INT unique,
  order_date DATE,
  customer_id INT,
  menu_id INT,
  qunatity INT);


--Insert data to customers table
INSERT INTO customers VALUES
  (01, 'Ahmed', 'Al-Din', 25, 'Male', TRUE),
  (02, 'Mohamed', 'Alli', 50, 'Male', FALSE),
  (03, 'Sarah', 'Van-Der-Waal', 30, 'Female', TRUE),
  (04, 'Toy', 'Datarockie', 30, 'Male', FALSE),
  (05, 'Sam', 'Lockheart', 28, 'Male',TRUE),
  (06, 'John', 'Doe', 30, 'Male', FALSE),
  (07, 'Bill', 'Gates', 65,'Male', TRUE),
  (08, 'Mary', 'Ann', 25, 'Female', FALSE),
  (09, 'David', 'Beckham', 60, 'Male', TRUE),
  (10, 'Jeff', 'Bezos', 65, 'Male', FALSE);

--Insert data to menu table
INSERT INTO menu VALUES
  (01, 'Margherita', 250),
  (02, '4 Cheese', 280),
  (03, 'Meat Lovers', 300),
  (04, 'Prociutto', 320),
  (05, 'Smoked Salmon', 380),
  (06, 'Hawaiian', 300),
  (07, 'Pepporoni',280),
  (08, 'BBQ Chicken', 300);

-- Insert data to order table
INSERT INTO orders VALUES
  (01, '2022-08-01', 01, 01, 2),
  (02, '2022-08-01', 02, 02, 1),
  (03, '2022-08-01', 02, 02, 1),
  (04, '2022-08-01', 04, 02, 1),
  (05, '2022-08-01', 05, 03, 4),
  (06, '2022-08-01', 05, 06, 2);

.mode box
/* SELECT * from customers;
SELECT * from menu;
select * from orders; */

-- MOST ORDERED AND TOTAL AMOUNT using JOIN and AGGREGATE Function
SELECT
  t2.name,
  t2.price,
  SUM(t3.qunatity) as qty,
  SUM(t2.price*t3.qunatity) as total
from menu t2
JOIN orders t3
ON t2.menu_id = t3.menu_id
GROUP BY 1
ORDER BY 3 DESC;

-- SUBQUERY
SELECT 
  id,
  name,
  lastname
FROM (select *
      from customers
     where member = true);

-- BILLING SYSTEM
select 
  t2.order_id,
  t1.name,
  t1.lastname,
  t3.name as menu,
  t3.price,
  t2.qunatity,
  t2.qunatity*t3.price as total
from customers t1
JOIN orders t2
ON t1.id = t2.customer_id
JOIN menu t3
ON t2.menu_id = t3.menu_id;
