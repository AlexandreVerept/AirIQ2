# AIRIQ 2

## 5_Frontend API

Here is our `Frontend API` code. This API can be freely access by any one, and allow us to consult the predictions we made with our `Prediction script`.

### List of commands:

| Command                                          | Type of request | Description                                                  | Return example                                               |
| ------------------------------------------------ | --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `/`                                              | GET             | Root of the API                                              | *"Welcome to our frontend API"*                              |
| `/allpredictions`                                | GET             | Get a dictionary with all the predictions made to this day with their `dateofprediction`, `typeofprediction`, `value`. | {"dateofprediction":{"0":"2020-04-10","1":"2020-04-09","2":"2020-04-09","3":"2020-04-08","4":"2020-04-08","5":"2020-04-07","6":"2020-04-04","7":"2020-04-03","8":"2020-04-02"},"typeofprediction":{"0":"J+3","1":"J+3","2":"J+2","3":"J+2","4":"J+1","5":"J+1","6":"J+3","7":"J+2","8":"J+1"},"value":{"0":4.9194,"1":4.59621,"2":5.85185,"3":4.46729,"4":5.47996,"5":3.7226,"6":2.70894,"7":3.14022,"8":4.22177}} |
| `/getprediction`  or `/getprediction/<nbOfDays>` | GET             | This method send all the predictions for the last X days in a JSON. The optional`<nbOfDays>` must be an int (0 by default). Please take not that 0 means that there is only the value of today. | {"dateofprediction":{"0":"2020-04-10","1":"2020-04-09","2":"2020-04-08"},"insertdate":{"0":"Tue, 07 Apr 2020 00:00:00 GMT","1":"Tue, 07 Apr 2020 00:00:00 GMT","2":"Tue, 07 Apr 2020 00:00:00 GMT"},"typeofprediction":{"0":"J+3","1":"J+2","2":"J+1"},"value":{"0":4.9194,"1":5.85185,"2":5.47996}} |



