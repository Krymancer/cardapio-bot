import requests
from bs4 import BeautifulSoup
from datetime import datetime

labels = [':cut_of_meat: OPÇÃO 01', ':poultry_leg: OPÇÃO 02', ':broccoli: VEGETARIANO', ':green_salad: SALADA',
          ':spaghetti: GUARNIÇÃO', ':rice: ACOMPANHAMENTOS', ':tangerine: SOBREMESA']


def getMenu():
    r = requests.get('http://www.sobral.ufc.br/ru/cardapio/')
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('tbody')

    lunchData = []
    dinnerData = []

    for br in soup.find_all('br'):  # Textos nos acompanhamentos são separados por <br>
        br.replace_with(' / ')

    lunch = tables[0].find_all('tr')
    dinner = tables[1].find_all('tr')

    for row in lunch:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        lunchData.append([ele for ele in cols if ele])

    for row in dinner:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        dinnerData.append([ele for ele in cols if ele])

    return lunchData, dinnerData


def getTodayDishes(date):
    almoco, jantar = getMenu()

    i = almoco[0].index(date)

    lunchDishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                     for dishes in almoco[1:]]

    dinnerDishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                     for dishes in jantar[1:]]

    return {'almoco': dict(zip(labels, lunchDishes)),
            'janta': dict(zip(labels, dinnerDishes))}


def getDate():
    today = datetime.today()
    return today.strftime('%d/%m')
