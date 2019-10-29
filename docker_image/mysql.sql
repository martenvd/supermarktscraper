CREATE DATABASE producten;
USE producten;
CREATE TABLE albert_heijn (
	productnaam VARCHAR(255) NOT NULL,
	prijs FLOAT(6,2) NOT NULL,
	product_url VARCHAR(1023),
	gewicht INT(6),
	imagelink VARCHAR(1023)
);
CREATE USER 's4dpython'@'%' IDENTIFIED BY 's4dpython';
GRANT ALL PRIVILEGES ON producten.* TO 's4dpython'@'%';
FLUSH PRIVILEGES;