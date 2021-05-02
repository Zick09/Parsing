from bs4 import BeautifulSoup
import requests
import os
import pandas as pd


# URL = 'https://auto.ru/cars/honda/accord/6306860/all/?displacement_from=2400'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
FILE = 'cars.xlsx'


def get_html(url, params=None):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ListingItem-module__main')
    cars = []
    for i in items:
        if i.find('div', class_='ListingItemPrice-module__content'):
            price = i.find('div', class_='ListingItemPrice-module__content').get_text()
        else:
            price = 'Цену уточняйте'

        if i.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp'):
            city = i.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').get_text()
        else:
            city = 'Город неизвестен'
        cars.append({
            'title': i.find('a', class_='Link ListingItemTitle-module__link').get_text().replace('Ð', 'Р'),
            'link': i.find('a', class_='Link ListingItemTitle-module__link').get('href'),
            'price': price,
            'city': city
        })
    return cars


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='Button__text')
    if pagination:
        return int(pagination[-4].get_text())
    else:
        return 1


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        df = pd.DataFrame()
        col = ['title', 'link', 'price', 'city']
        for i in items:
            ser = [i['title'], i['link'], i['price'], i['city']]
            temp_df = pd.DataFrame([ser], columns=col)
            df = df.append(temp_df)
        writer = pd.ExcelWriter('cars.xlsx', engine= 'xlsxwriter')
        df.to_excel(writer, sheet_name='1', index=False)
        writer.save()


def parse():
    URL = input('Введите URL: ')
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1,pages_count+1):
            print(f'Parsing page {page} from {pages_count}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        print(cars)
        print(f'Получено {len(cars)} автомобилей')
        save_file(cars, FILE)
    else:
        'Error'
    print(cars)
    os.startfile(FILE)


parse()
