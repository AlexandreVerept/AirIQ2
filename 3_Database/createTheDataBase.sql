CREATE DATABASE IF NOT EXISTS airiq;

USE airiq;

CREATE TABLE IF NOT EXISTS iqtable (
	value INT NOT NULL CHECK(value>=0 and value<=10),
	date DATE NOT NULL UNIQUE,
	PRIMARY KEY (date));
    
CREATE TABLE IF NOT EXISTS synoptable (
	pressure INT NOT NULL CHECK(pressure>=0),
    wind_direction INT NOT NULL CHECK(wind_direction>=0 and wind_direction<=360),
    wind_force float NOT NULL CHECK(wind_force>=0),
    humidity float NOT NULL CHECK (humidity>=0 and humidity<=100),
    temperature float NOT NULL CHECK (temperature>0),
	date VARCHAR(19) NOT NULL UNIQUE,
	PRIMARY KEY (date));
    
CREATE TABLE IF NOT EXISTS predictiontable (
	id INT AUTO_INCREMENT,
	value FLOAT NOT NULL CHECK(value>=0 and value<=10),
    dateofprediction DATE NOT NULL,
    typeofprediction VARCHAR(3) NOT NULL CHECK(typeofprediction='J+1' or typeofprediction='J+2' or typeofprediction='J+3'),
	insertdate DATE,
	PRIMARY KEY (id));