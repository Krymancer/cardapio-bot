import requests
from bs4 import BeautifulSoup
from datetime import datetime

labels = [':cut_of_meat: OPÇÃO 01', ':poultry_leg: OPÇÃO 02', ':broccoli: VEGETARIANO', ':green_salad: SALADA',
          ':spaghetti: GUARNIÇÃO', ':rice: ACOMPANHAMENTOS', ':tangerine: SOBREMESA']


def get_menu():
    r = requests.get('http://www.sobral.ufc.br/ru/cardapio')

    if r.status_code != 200:
        print('Error: cant get data from site')
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('tbody')

    lunch_data = []
    dinner_data = []

    for br in soup.find_all('br'):  # Textos nos acompanhamentos são separados por <br>
        br.replace_with(' / ')

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


def get_today_dishes(date):
    menu = get_menu()
    if menu is None:
        return None
        
    from pprint import pprint
    pprint(menu)

    almoco, jantar = menu
    almojoformated,jantarformated = []

    for item in almoco[0]:
        almojoformated.append(item[:5])

    for item in jantar[0]:
        jantarformated.append(item[:5])
    
    print("format",almojoformated[0])
    try:

        i = almojoformated[0].index(date)

        lunch_dishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                        for dishes in almoco[1:]]

        dinner_dishes = [dishes[i].replace('**', ':heavy_exclamation_mark:').replace('*', ':bangbang:')
                         for dishes in jantar[1:]]

        return {'almoco': dict(zip(labels, lunch_dishes)),
                'janta': dict(zip(labels, dinner_dishes))}
    except ValueError:
        print('Error: no dishes for', date)


def get_date():
    today = datetime.today()
    return today.strftime('%d/%m')


def get_hour():
    today = datetime.today()
    return today.strftime('%H:%M')
