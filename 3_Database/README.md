# AIRIQ 2

## 3_Database

Here are the SQL scripts needed to create our `Database` in which we stock all our data for real-time predictions. The database name is `airiq`

### The different tables:

#### iqtable

| value        | date (primary key) |
| ------------ | ------------------ |
| INT NOT NULL | DATE NOT NULL      |

#### synoptable

| pressure     | wind_direction | wind_force     | humidity       | temperature    | date (primary key) |
| ------------ | -------------- | -------------- | -------------- | -------------- | ------------------ |
| INT NOT NULL | INT NOT NULL   | FLOAT NOT NULL | FLOAT NOT NULL | FLOAT NOT NULL | DATE NOT NULL      |

#### poltable

| NO2          | O3           | PM10         | date (primary key) |
| ------------ | ------------ | ------------ | ------------------ |
| INT NOT NULL | INT NOT NULL | INT NOT NULL | DATE NOT NULL      |

#### predictiontable

| id (primary key)   | value          | dateofprediction | typeofprediction    | insertdate |
| ------------------ | -------------- | ---------------- | ------------------- | ---------- |
| INT AUTO_INCREMENT | FLOAT NOT NULL | DATE NOT NULL    | VARCHAR(3) NOT NULL | DATE       |

