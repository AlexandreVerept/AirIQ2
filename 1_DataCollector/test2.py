import csv
import requests

dateRequest = 20200310
CSV_URL = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.{}09.csv".format(str(dateRequest))


with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)