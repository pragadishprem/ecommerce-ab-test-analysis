-- Drop the database if it exists (This will delete ALL data in the database!)
DROP DATABASE IF EXISTS ecom_ab_test;

-- Create the database if it doesn't exist
CREATE DATABASE ecom_ab_test;

-- Select the database to use for subsequent operations
USE ecom_ab_test;

-- Create the orders table to store A/B test data
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_date DATE,
    order_value DECIMAL(10 , 2 ),
    test_variant VARCHAR(1),
    device_type VARCHAR(20),
    location VARCHAR(50),
    acquisition_channel VARCHAR(50),
    number_of_items INT,
    product_category VARCHAR(50)
);