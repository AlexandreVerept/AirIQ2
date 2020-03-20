USE airiq;

INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-21",'J+1');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(2,"2020-03-22",'J+2');
INSERT INTO predictiontable (value,dateofprediction,typeofprediction) VALUES(3,"2020-03-23",'J+3');

INSERT INTO iqtable (value,date) VALUES(2,"2020-03-20");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-19");
INSERT INTO iqtable (value,date) VALUES(3,"2020-03-18");

INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(101990,5.2,100,"2020-03-20");
INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(102930,6.1,340,"2020-03-19");
INSERT INTO synoptable (pressure,wind_direction,wind_force,date) VALUES(103160,4.2,15,"2020-03-18");

select * from predictiontable;
select * from iqtable;
select * from synoptable;