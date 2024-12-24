from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://pizzapizzburg.ru/menu/pizza'

# Делаем запрос и получаем html
html_text = requests.get(url).text

soup = BeautifulSoup(html_text, 'lxml')

# Находим объявления
ads = soup.find_all('div', class_='col-12 col-sm-6 col-lg-4 col-xxl-3 col-xxxl-2_5')

# Создаем список для хранения информации о пиццах
result = []

# Получаем все элементы
for ad in ads:
    pizza_name = ad.find('div', class_='product-unit__title js--basket-product__title').text.strip().split('\n')[0]

    price = ad.find('span', class_='js--product-price')
    price = price.text.replace(' ', '').strip() if price else "Цена не найдена"

    ingredients = ad.find('div', class_='product-unit__info').text.strip()

    result.append({
        "pizza_name": pizza_name,
        "price": price,
        "ingredients": ingredients
    })

# Преобразование в датафрейм
df = pd.DataFrame(result)

# Экспорт в CSV
filename = 'test.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig')