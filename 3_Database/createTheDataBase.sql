CREATE DATABASE IF NOT EXISTS airiq;

USE airiq;

CREATE TABLE IF NOT EXISTS iqtable (
	value INT NOT NULL CHECK(value>=0 and value<=10),
	date DATE NOT NULL UNIQUE,
	PRIMARY KEY (date));
    
CREATE TABLE IF NOT EXISTS predictiontable (
	id INT AUTO_INCREMENT,
	value FLOAT NOT NULL CHECK(value>=0 and value<=10),
    dateofprediction DATE NOT NULL,
    typeofprediction VARCHAR(3) NOT NULL CHECK(typeofprediction='J+1' or typeofprediction='J+2' or typeofprediction='J+3'),
	insertdate DATE DEFAULT (CURRENT_DATE),
	PRIMARY KEY (id));