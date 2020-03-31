USE airiq;

INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-21",'J+1');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-22",'J+2');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(3,"2020-03-23",'J+3');

INSERT INTO iqtable (value,date) VALUES(2,"2020-03-20");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-19");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-18");

INSERT INTO synoptable (pressure,wind_force,wind_direction,date,humidity,temperature) VALUES(101990,5.2,100,"2020-03-20 06:00:00","89","283");
INSERT INTO synoptable (pressure,wind_force,wind_direction,date,humidity,temperature) VALUES(102930,6.1,340,"2020-03-19 06:00:00","90","284.2");
INSERT INTO synoptable (pressure,wind_force,wind_direction,date,humidity,temperature) VALUES(103160,4.2,15,"2020-03-18 06:00:00","71","290.1");

select * from predictiontable;
select * from iqtable;
select * from synoptable;