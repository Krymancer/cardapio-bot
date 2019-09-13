import requests
from bs4 import BeautifulSoup
from datetime import datetime

labels = [':cut_of_meat: OPÇÃO 01', ':poultry_leg: OPÇÃO 02', ':broccoli: VEGETARIANO', ':green_salad: SALADA',
          ':spaghetti: GUARNIÇÃO', ':rice: ACOMPANHAMENTOS', ':tangerine: SOBREMESA']


def getMenu():
    r = requests.get('http://www.sobral.ufc.br/ru/cardapio/')
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('tbody')

    almoco_data = []
    jantar_data = []

    for br in soup.find_all('br'):  # Textos nos acompanhamentos são separados por <br>
        br.replace_with(' / ')

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

    return almoco_data, jantar_data


def getTodayDishes(date):
    almoco, jantar = getMenu()

    i = almoco[0].index(date)

    almoco_dishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                     for dishes in almoco[1:]]

    jantar_dishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                     for dishes in jantar[1:]]

    return {'almoco': dict(zip(labels, almoco_dishes)),
            'janta': dict(zip(labels, jantar_dishes))}


def getDate():
    today = datetime.today()
    return today.strftime('%d/%m')
