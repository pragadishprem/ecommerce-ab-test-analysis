SELECT 
    *
FROM
    orders;

SELECT 
    test_variant,
    AVG(order_value) AS average_order_value,
    COUNT(*) AS sample_size
FROM
    orders
GROUP BY test_variant;

SELECT 
    order_date,
    test_variant,
    AVG(order_value) AS daily_average_order_value
FROM
    orders
GROUP BY order_date , test_variant
ORDER BY order_date , test_variant;

SELECT 
    order_value
FROM
    orders
WHERE
    test_variant = 'A';

SELECT 
    order_value
FROM
    orders
WHERE
    test_variant = 'B';


