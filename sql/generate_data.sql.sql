DROP PROCEDURE IF EXISTS generate_test_data;

DELIMITER //
CREATE PROCEDURE generate_test_data(IN num_rows INT)
BEGIN
    DECLARE i INT DEFAULT 1;

    -- Constants for the variables
    DECLARE num_users INT DEFAULT 100;
    DECLARE max_items_per_order INT DEFAULT 10;

    -- Use this values for the set numbers, these will be the actual values from the random statements
    DECLARE device_types VARCHAR(255) DEFAULT 'desktop,mobile,tablet';
    DECLARE locations VARCHAR(255) DEFAULT 'USA,Canada,UK,Germany,France';
    DECLARE acquisition_channels VARCHAR(255) DEFAULT 'organic search,paid advertising,email marketing,social media,referral';
    DECLARE product_categories VARCHAR(255) DEFAULT 'Electronics,Clothing,Books,Home Goods,Beauty,Sports';

    WHILE i <= num_rows DO
        -- User and Date
        SET @user_id = FLOOR(RAND() * num_users) + 1;
        SET @order_date = DATE(NOW() - INTERVAL FLOOR(RAND() * 30) DAY);

        -- A/B value
        SET @test_variant = IF(RAND() > 0.5, 'A', 'B');

        -- New method for getting a correct distribution
        SET @device_type = ELT(FLOOR(1 + RAND() * 3), 'desktop', 'mobile', 'tablet');
        SET @location = ELT(FLOOR(1 + RAND() * 5), 'USA', 'Canada', 'UK', 'Germany', 'France');
        SET @acquisition_channel = ELT(FLOOR(1 + RAND() * 5), 'organic search', 'paid advertising', 'email marketing', 'social media', 'referral');
        SET @product_category = ELT(FLOOR(1 + RAND() * 6), 'Electronics', 'Clothing', 'Books', 'Home Goods', 'Beauty', 'Sports');

       SET @number_of_items = FLOOR(RAND() * max_items_per_order) + 1;

        -- Base order value
        SET @base_order_value = (RAND() * 50) + 10;
        SET @order_value = @base_order_value;

        -- Use some assumptions
        IF @product_category = 'Electronics' THEN
            SET @order_value = @order_value * (3.5 + RAND() * 1.5);
        END IF;

        -- Random values, but higher a referral link is sent
        IF @acquisition_channel = 'referral' THEN
            SET @order_value = @order_value * (1.4 + RAND() * 0.4);
        END IF;

        -- Check for device test and then test those too.
        IF @test_variant = 'A' AND @device_type = 'mobile' THEN
            SET @order_value = @order_value * 0.9;
        END IF;

        SET @order_value = @order_value * @number_of_items;
        SET @order_value = ROUND(@order_value, 2);

        -- Load them all in
        INSERT INTO orders (user_id, order_date, order_value, test_variant, device_type, location, acquisition_channel, number_of_items, product_category)
        VALUES (@user_id, @order_date, @order_value, @test_variant, @device_type, @location, @acquisition_channel, @number_of_items, @product_category);

        SET i = i + 1;
    END WHILE; END
//

DELIMITER ;

CALL generate_test_data(1000);