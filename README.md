# AIRIQ 2

## Goal of this student project

This is a first year of master research project done by **Mohamed Boulanouar**, **Maxime Thoor** and **Alexandre Verept**, supervised by **Kévin Hérissé** (PhD student) at [**ISEN**](https://www.isen-lille.fr/) engineering school.

The goal of this project is **to predict the air quality** 1, 2 and 3 days in advance in Lille **with the highest accuracy as possible**. 

In a way to accomplish this, we will use some machine learning and statistical techniques.

<img src="https://t1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/IgT/image/I0UJ8f2U5ePsX3LU-kJS--yIarU.png" alt="r" style="zoom:45%;" />

**NB:** Here you can find **[our first semester project](https://github.com/AlexandreVerept/Projet-AirIQ)**, that consisted in the forecasting of the Air Index quality in Lille, based on only few data collected by a bee hive placed on the roof of the school. We had the chance to present our project in a public event organized by the MEL (*Metropole Européenne de Lille*).

![Jeudi du Numérique](Pictures\JDN.jpg)

## Final product architecture

Here is the general structure of our solution:

![Architecture](Pictures/architecture.png)

**Data Collector:**

- This script is running in <u>real time</u> and collect all the data from different APIs, shape them if needed, then send the result to our `Backend API` to be stored in the `Database`.

**Backend API:**

- <u>Receive useful data</u> from the `Data Collector` to store it in the `Data base`.
- <u>Provide data</u> to our real time `Prediction script`, <u>receive the results of the predictions</u> and store them in the `Data base`.
- This API is <u>password protected</u> as it should only be used by us.

**Data Base:**

- <u>MySQL database</u> used to <u>store all the data we need</u>: the different open source datasets, predictions ...

**Front End API:**

- Used to <u>consult freely</u> our predictions stored in the `Database` (without password).

**Final display:**

- If we have time, it could be interesting to create a website/application to see our predictions.

  

## Open data

The datasets we use must be a real time data to be useful for the prediction, but we also need archived data over a long period of time in a way to create a training dataset for our predictive model.

**Potential open data APIs to exploit :**

| Name                                                         | Source       | Description                                                  | Frequency               | Time frame        |
| ------------------------------------------------------------ | ------------ | ------------------------------------------------------------ | ----------------------- | ----------------- |
| [*Indice qualité de l'air*](https://opendata.lillemetropole.fr/explore/dataset/indice-qualite-de-lair/table/?rows=10000&lang=&sort=date_ech) | MEL          | Air index quality                                            | Every day               | Window of 2 years |
| *[Pluviométrie MEL](https://opendata.lillemetropole.fr/explore/dataset/pluviometrie/table/?sort=date&refine.nom=LILLE)* | MEL          | Pluviometry level (multiple time each hour - window of 2 years) | Multiple time each hour | Window of 2 years |
| *[Mesures journalières des principaux polluants](https://opendata.lillemetropole.fr/explore/dataset/mesures-journalieres-des-principaux-polluants/table/?sort=date_fin&refine.nom_com=Lille&refine.nom_station=Lille+Leeds)* | MEL          | Value of the main pollutants                                 | Every day               | Window of 2 years |
| *[Données SYNOP Essentielles OMM](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32)* | Météo France | Wide range of weather data including wind, pressure, humidity and temperature | Every 3 hours           | Since 1997        |



