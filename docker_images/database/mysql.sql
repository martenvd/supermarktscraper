CREATE DATABASE producten;
USE producten;
CREATE TABLE albert_heijn (
	productnaam VARCHAR(255) NOT NULL,
	prijs FLOAT(6,2) NOT NULL,
	product_url VARCHAR(1023),
	hoeveelheid VARCHAR(255),
	imagelink VARCHAR(1023)
);
CREATE TABLE aldi (
	productnaam VARCHAR(255) NOT NULL,
	prijs FLOAT(6,2) NOT NULL,
	product_url VARCHAR(1023),
	imagelink VARCHAR(1023)
);
CREATE TABLE jumbo (
	productnaam VARCHAR(255) NOT NULL,
	prijs FLOAT(6,2) NOT NULL,
	product_url VARCHAR(1023),
	hoeveelheid VARCHAR(255),
	imagelink VARCHAR(1023)
);
CREATE TABLE coop (
	productnaam VARCHAR(255) NOT NULL,
	prijs FLOAT(6,2) NOT NULL,
	product_url VARCHAR(1023),
	hoeveelheid VARCHAR(255),
	imagelink VARCHAR(1023)
);
CREATE USER 's4dpython'@'%' IDENTIFIED BY 's4dpython';
GRANT ALL PRIVILEGES ON producten.* TO 's4dpython'@'%';
FLUSH PRIVILEGES;
