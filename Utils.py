import requests
from bs4 import BeautifulSoup
from datetime import datetime


def getMenu():
    r = requests.get('http://www.sobral.ufc.br/ru/cardapio/')
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('tbody')

    lunch_data = []
    dinner_data = []

    lunch = tables[0].find_all('tr')
    dinner = tables[1].find_all('tr')

    for row in lunch:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        lunch_data.append([ele for ele in cols if ele])

    for row in dinner:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        dinner_data.append([ele for ele in cols if ele])

    return lunch_data, dinner_data

def getTodayDishes(date):
    lunch,dinner = getMenu()
    lunch_dishes = []
    dinner_dishes = []

    i = -1
    for index,col in enumerate(lunch[0]):
        if col == date:
            i = index

    for dishes in lunch[1:]:
        lunch_dishes.append(dishes[i])

    for dishes in dinner[1:]:
        dinner_dishes.append(dishes[i])

    return lunch_dishes,dinner_dishes


def getDateHour():
    today = datetime.today()
    return today.strftime('%d/%m'), today.strftime('%H:%M')