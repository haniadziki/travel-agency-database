DROP TABLE IF EXISTS finance;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;

CREATE TABLE country (
    country_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    country VARCHAR(20) NOT NULL
);

CREATE TABLE city (
    city_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(30) NOT NULL,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE address (
    address_id int AUTO_INCREMENT PRIMARY KEY,
    address varchar(255),
    city_id int,
    postal_code varchar(15),
    phone varchar(15),
    FOREIGN KEY (city_id) REFERENCES city(city_id));

CREATE TABLE customers (
    customer_id int AUTO_INCREMENT PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    address_id int,
    FOREIGN KEY (address_id) REFERENCES address(address_id));

CREATE TABLE staff (
    staff_id int AUTO_INCREMENT PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    address_id int,
    FOREIGN KEY (address_id) REFERENCES address(address_id));

CREATE TABLE offers (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    duration_length INT,
    plane_number INT,
    plane_price INT,
    attractions VARCHAR(255),
    attractions_price INT,
    hotel_name VARCHAR(255),
    hotel_price INT,
    original_price INT,
    overall_price INT,
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    offer_id INT,
    customer_id INT,
    staff_id INT,
    order_date DATETIME,
    trip_start DATETIME,
    trip_end DATETIME,
    FOREIGN KEY (offer_id) REFERENCES offers(offer_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE salary (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    salary INT
);

CREATE TABLE finance (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    balance INT
);
