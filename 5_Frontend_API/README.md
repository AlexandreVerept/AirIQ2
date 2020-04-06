# AIRIQ 2

## 5_Frontend API

Here is our `Frontend API` code. This API can be freely access by any one, and allow us to consult the predictions we made with our `Prediction script`.

### List of commands:

| Command                                          | Type of request | Description                                                  | Return example                                               |
| ------------------------------------------------ | --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `/`                                              | GET             | Root of the API                                              | *"Welcome to our frontend API"*                              |
| `/allpredictions`                                | GET             | Get a dictionary with all the predictions made to this day with their `dateofprediction`, `typeofprediction`, `value`. | *{"dateofprediction":{"0":"Wed, 11 Mar 2020 00:00:00 GMT","1":"Tue, 10 Mar 2020 00:00:00 GMT","2":"Mon, 09 Mar 2020 00:00:00 GMT"},"typeofprediction":{"0":"J+3","1":"J+2","2":"J+1"},"value":{"0":3.0,"1":2.0,"2":2.0}}* |
| `/getprediction`  or `/getprediction/<nbOfDays>` | GET             | This method send all the predictions for the last X days in a JSON. The optional`<nbOfDays>` must be an int (0 by default). Please take not that 0 means that there is only the value of today. | {"dateofprediction":{"0":"Thu, 09 Apr 2020 00:00:00 GMT","1":"Wed, 08 Apr 2020 00:00:00 GMT","2":"Tue, 07 Apr 2020 00:00:00 GMT"},"insertdate":{"0":"Mon, 06 Apr 2020 00:00:00 GMT","1":"Mon, 06 Apr 2020 00:00:00 GMT","2":"Mon, 06 Apr 2020 00:00:00 GMT"},"typeofprediction":{"0":"J+3","1":"J+2","2":"J+1"},"value":{"0":4.59621,"1":4.46729,"2":3.7226}} |



