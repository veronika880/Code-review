from flask import Flask, render_template, request
import pandas as pd
import sqlite3

app = Flask(__name__)

# Путь к базе данных SQLite
db_path = 'data/pizza.db'


# Загружаем данные из CSV в базу данных (если необходимо)
def load_data_to_db():
    df = pd.read_csv('test.csv')
    conn = sqlite3.connect(db_path)
    df.to_sql('pizzas', conn, if_exists='replace', index=False)
    conn.close()


load_data_to_db()


@app.route('/')
def index():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql('SELECT * FROM pizzas', conn)
    conn.close()

    df['price'] = df['price'].astype(float)
    df_sorted = df.sort_values(by='price')

    cheapest_pizza = df_sorted.iloc[0]
    most_expensive_pizza = df_sorted.iloc[-1]

    # Получаем параметры сортировки из URL
    sort_by = request.args.get('sort_by', 'price')  # По умолчанию сортировка по цене
    order = request.args.get('order', 'asc')  # По умолчанию по возрастанию

    # Сортируем датафрейм
    if sort_by == 'name':
        df_sorted = df.sort_values(by='pizza_name', ascending=(order == 'asc'))
    else:
        df_sorted = df.sort_values(by='price', ascending=(order == 'asc'))

    return render_template('index.html', tables=[df_sorted.to_html(classes='data')],
                           titles=df_sorted.columns.values, cheapest_pizza=cheapest_pizza,
                           most_expensive_pizza=most_expensive_pizza)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

