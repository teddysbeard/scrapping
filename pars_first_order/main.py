import csv
import datetime
import json
import random
from time import sleep
import requests
from bs4 import BeautifulSoup

url = "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?place=0-1&page=0&limit=100&sortName=objReady100PercDt&sortDirection=desc&objectIds=44604%2C39212%2C41181"

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31'
}

# req = requests.Session().get(url, headers=headers)  # сохраним полученный объект в переменную и применим метод text.
# src = req.text
# print(src)
# Соханим полученные данные, покольку многие сайты могут дать бан за большое количество
# запросов при парсниге
# with open('page.html', 'w') as file:
#     file.write(src)
with open('page.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_id_soup = soup.find_all('span',
                            class_='styles__Ellipsis-sc-1fw79ul-0 cDcbYl styles__Child-sc-cx1nz2-0 styles__Primary-sc-cx1nz2-1 bcibid')
all_pd_soup = soup.find_all("span",
                            class_="styles__Ellipsis-sc-1fw79ul-0 cDcbYl styles__Child-sc-cx1nz2-0 styles__Secondary-sc-cx1nz2-2 hyjkdD")
all_developers_soup = soup.find_all("span",
                                    class_="styles__Ellipsis-sc-1fw79ul-0 cDcbYl styles__Child-sc-b0i2cq-0 styles__Primary-sc-b0i2cq-1 hvMGzU")

all_id = [i.text for i in all_id_soup]
all_pd = [i.text for i in all_pd_soup]
all_developers = [i.text for i in all_developers_soup]
all_stages_and_flats = soup.find_all("div", class_="styles__Cell-sc-7809tj-0 ibavEN Newbuindings Newbuildings_small")

all_stages = [all_stages_and_flats[i].text for i in range(len(all_stages_and_flats)) if i % 2 == 0]
all_flats = [all_stages_and_flats[i].text for i in range(len(all_stages_and_flats)) if i % 2 != 0]
print(all_id)
print(all_pd)
print(all_developers)
print(all_stages)
print(all_flats)

all_address_areas_and_commissioning = soup.find_all("div",
                                                    class_="styles__Cell-sc-7809tj-0 ibavEN Newbuindings BuildersTable_normal",
                                                    )
all_refs = soup.find_all("a", class_="styles__Address-sc-j3mki0-0 hLRgrJ")

all_refs = [i.get('href') for i in all_refs]
print(len(all_refs), all_refs)

print(type(all_address_areas_and_commissioning))
all_address = [i.text for i in all_address_areas_and_commissioning[::3]]

all_hrefs = [i.get("href") for i in all_address_areas_and_commissioning[::3]]
all_areas = [i.text for i in all_address_areas_and_commissioning[1::3]]

all_commissioning = [i.text for i in all_address_areas_and_commissioning[2::3]]
counter = 1

print(all_address)
print(all_areas)
print(all_commissioning)
print(all_hrefs)

#  Создание и запись в файл CSV полученных данных
with open("New_buildings.csv", "w", encoding="utf-8") as file:
    csv.excel.delimiter = ','
    writer = csv.writer(file, dialect=csv.excel)
    # Метод ниже принимает лишь один аргумент, как передать ему 5? Запишем их в список или кортеж
    writer.writerow(
        (
            "!D",
            "PD",
            "Address",
            "Developer",
            "Stages",
            "Flats",
            "Total area",
            "Commissioning"
        )
    )
for i in range(len(all_id)):
    with open("New_buildings.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Метод ниже принимает лишь один аргумент, как передать ему 5? Запишем их в список или кортеж
        writer.writerow(
            (
                all_id[i],
                all_pd[i],
                all_address[i],
                all_developers[i],
                all_stages[i],
                all_flats[i],
                all_areas[i],
                all_commissioning[i]
            )
        )
