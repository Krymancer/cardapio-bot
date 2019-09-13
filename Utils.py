import requests
from bs4 import BeautifulSoup
from datetime import datetime


def getMenu():
    r = requests.get('http://www.sobral.ufc.br/ru/cardapio/')
    soup = BeautifulSoup(r.text, 'html.parser')
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

    return almoco_data, jantar_data

def getTodayDishes(date):
    almoco,jantar = getMenu()
    almoco_dishes = []
    jantar_dishes = []

    i = -1
    for index,col in enumerate(almoco[0]):
        if col == date:
            i = index

    for dishes in almoco[1:]:
        almoco_dishes.append(dishes[i])

    for dishes in jantar[1:]:
        jantar_dishes.append(dishes[i])

    return almoco_dishes,jantar_dishes


def getDateHour():
    today = datetime.today()
    return today.strftime('%d/%m')#, today.strftime('%H:%M')