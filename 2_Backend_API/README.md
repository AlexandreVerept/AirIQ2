# AIRIQ 2

## 2_Backend_API

Here you can find the API that receive various data from the `DataCollector` or our `PredictionScript` in a way to store them in our `Database`.

This API will be protected by a password.

| Command                     | Type of request | Description                                                  | Return example                                               |
| --------------------------- | --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `/`                         | GET             | Root of the API                                              | *"Welcome to our backend API"*                               |
| `/test`                     | POST            | This command is just here to test our POST methods in other scripts. It receive a JSON and send it back. | *{"test":"123"}*                                             |
| `/prediction`               | GET             | This method send all the information needed to make one prediction. It send a list of JSON. | [{"date":{"0":"Fri, 20 Mar 2020 00:00:00 GMT","1":"Thu, 19 Mar 2020 00:00:00 GMT"},"value":{"0":2,"1":3}},{"date":{"0":"Fri, 20 Mar 2020 00:00:00 GMT","1":"Thu, 19 Mar 2020 00:00:00 GMT"},"pressure":{"0":101990,"1":102930},"wind_direction":{"0":5,"1":6},"wind_force":{"0":100.0,"1":340.0}}] |
| `/realtimepredictions`      | POST            | Receive a JSON file with a prediction with: `IQ+1`, `IQ+2`, `IQ+3`, `date`. | *200*                                                        |
| `/infodatacollector/<type>` | POST            | Receive a JSON file with information coming from the `dataCollector`. The parameter `<type>` must be "*iq"*, *"pollutant"* or *"synop"*. | *200*                                                        |