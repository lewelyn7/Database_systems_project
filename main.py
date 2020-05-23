import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://syllabuskrk.agh.edu.pl/2019-2020/pl/magnesite/study_plans/stacjonarne-informatyka'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table')

for table in tables:
    semnumid = table.get('id')
    semnum = str(semnumid)
    splitted = semnum.split("-")
    print(splitted[2])

    tds = table.find_all('td', class_="subject_name")
    for td in tds:
        ahref = td.find('a')
        print(ahref.text + ";" + splitted[2])

