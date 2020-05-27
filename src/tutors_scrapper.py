import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://skos.agh.edu.pl/jednostka/akademia-gorniczo-hutnicza-im-stanislawa-staszica-w-krakowie/wydzial-fizyki-i-informatyki-stosowanej/katedra-fizyki-medycznej-i-biofizyki-339.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('li')

outfile=open("wykladowcy3.csv","w")
csvwriter = csv.writer(outfile)

for table in tables:
    ahref = str(table.find('a'))
    splitted = ahref.split(">")
    
    if(len(splitted)==3):
        splitted2=splitted[1].split(',')

        if(len(splitted2)==2):
            title=splitted2[1][1:-3]
            namesurname=splitted2[0].split(' ')
            mail=namesurname[1][0].lower()+namesurname[0].lower()+"@agh.edu.pl"
            csvwriter.writerow([namesurname[0],namesurname[1],title,mail])
        
    
