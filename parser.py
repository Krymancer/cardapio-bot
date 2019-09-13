import requests 
from bs4 import BeautifulSoup

r = requests.get('http://www.sobral.ufc.br/ru/cardapio/')
soup = BeautifulSoup(r.text,'html.parser')
tables = soup.find_all('tbody')

almoco_data = []
jantar_data = []

almoco = tables[0].find_all('tr')
jantar = tables[1].find_all('tr')

for row in almoco:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    almoco_data.append([ele for ele in cols if ele])

for row in jantar:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    jantar_data.append([ele for ele in cols if ele])


for rows in almoco_data:
    print(rows)

for rows in jantar_data:
    print(rows)
