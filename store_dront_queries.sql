-- CREATE DATABASE store_front; 
USE store_front; 

-- CREATE TABLE categories(
-- 	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
--     name VARCHAR(30)
-- );

-- INSERT INTO categories
-- VALUES(NULL, "Furniture");

-- INSERT INTO categories
-- VALUES(NULL, "Clothing");


-- DELETE FROM categories WHERE id=2;


CREATE TABLE products(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title VARCHAR(30),
    description VARCHAR(250),
    price INT,
    img_url VARCHAR(600),
    category INT,
    favorite ENUM('0', '1'),
    FOREIGN KEY (category) REFERENCES categories(id)
);

-- INSERT INTO products
-- VALUES(NULL, "chair","you sit on it",10,'www.google.com','furniture','1');
-- UPDATE products SET description = 'ijdfjnjnnsdnj' WHERE id = 1;
-- UPDATE products SET description = 'AFLjbLFBD' WHERE id = 1;

-- DROP TABLE products;
