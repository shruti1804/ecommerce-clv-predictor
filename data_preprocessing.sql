
-- 1. Create Customers Table
CREATE TABLE olist_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(50),
    customer_state VARCHAR(5)
);

-- 2. Create Orders Table
CREATE TABLE olist_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);
-- 3. Create Payments Table
CREATE TABLE olist_order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value NUMERIC(10,2)
);

-- 4. Create Master Dataset for CLV Analysis
WITH OrderPayments AS (
    -- Group multiple payments (installments) into a single total per order
	-- if one customer makes payment voucher + credit like this , it is grouped together as total payment to reduce confusion. 
    SELECT 
        order_id, 
        SUM(payment_value) AS total_payment
    FROM olist_order_payments
    GROUP BY order_id
)

-- Join everything together to create the Master Dataset
SELECT 
    c.customer_unique_id,
    o.order_id,
    o.order_purchase_timestamp,
    p.total_payment
FROM olist_orders o
JOIN olist_customers c 
    ON o.customer_id = c.customer_id
JOIN OrderPayments p 
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';