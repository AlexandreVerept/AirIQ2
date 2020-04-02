# AIRIQ 2

## 2_Backend_API

Here you can find the API that receive various data from the `DataCollector` or our `PredictionScript` in a way to store them in our `Database`.

This API will be protected by a password.

|                  Command                   | Type of request | Description                                                  | Return example                                               |
| :----------------------------------------: | :-------------: | :----------------------------------------------------------- | ------------------------------------------------------------ |
|                    `/`                     |       GET       | Root of the API                                              | *"Welcome to our backend API"*                               |
|                  `/test`                   |      POST       | This command is just here to test our POST methods in other scripts. It receive a JSON and send it back. | *{"test":"123"}*                                             |
| `/prediction`  or `/prediction/<nbOfDays>` |       GET       | This method send all the information needed to make one prediction. It send a list of JSON. The optional`<nbOfDays>` must be an int (2 by default). Note that this number means the number of days you want, in addition to the today's data. | [{"date":{"0":"Thu, 02 Apr 2020 00:00:00 GMT"},"value":{"0":5}},{"date":{"0":"2020-04-02 06:00:00","1":"2020-04-02 03:00:00","2":"2020-04-02 00:00:00"},"humidity":{"0":84.0,"1":85.0,"2":82.0},"pressure":{"0":101110,"1":101170,"2":101270},"temperature":{"0":276.05,"1":275.25,"2":274.55},"wind_direction":{"0":220,"1":160,"2":290},"wind_force":{"0":1.0,"1":0.5,"2":1.4}}] |
|           `/realtimepredictions`           |      POST       | Receive a JSON file with a prediction with: `IQ+1`, `IQ+2`, `IQ+3`, `date`. | *200*                                                        |
|        `/infodatacollector/<type>`         |      POST       | Receive a JSON file with information coming from the `dataCollector`. The parameter `<type>` must be "*iq"*, *"pollutant"* or *"synop"*. | *200*                                                        |