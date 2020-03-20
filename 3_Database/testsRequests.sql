USE airiq;

INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-9",'J+1');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-10",'J+2');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(3,"2020-03-11",'J+3');

INSERT INTO iqtable (value,date) VALUES(2,"2020-03-9");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-10");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-11");

INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(101990,5.2,100,"2020-03-9");
INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(102930,6.1,340,"2020-03-10");
INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(103160,4.2,15,"2020-03-11");

select * from predictiontable;
select * from iqtable;
select * from synoptable;