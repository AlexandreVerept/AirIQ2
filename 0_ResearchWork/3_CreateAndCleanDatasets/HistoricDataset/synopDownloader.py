"""
 This program allow us to download historics SYNOP infomations from MétéoFrance
"""

import requests
import gzip

print('Download Starting...')

URL = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/'

def loadFile(filename):
    try:
        r = requests.get(URL+"/"+filename)
        with gzip.open("synop/"+filename,'wb') as output_file:
            output_file.write(r.content)
        print(filename + ' - completed')
    except:
        print(filename + ' - ERROR')
    

for year in range (1996,2021):
    for month in range(1,10):
        filename = "synop."+ str(year)+'0'+str(month)+ ".csv.gz"
        loadFile(filename)
    for month in range(10,13):
        date = str(year) + str(month)        
        filename = "synop."+ str(year)+str(month)+ ".csv.gz"
        loadFile(filename)
        
        
