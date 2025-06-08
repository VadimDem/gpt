import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# ----- create tables -----
cur.execute(
    '''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )'''
)

cur.execute(
    '''CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        description TEXT,
        image TEXT,
        category TEXT
    )'''
)

# ----- seed products -----
products = [
    ('Ведро', 100, 'Пластиковое ведро 10л', 'images/bucket.png', 'уборка'),
    ('Швабра', 200, 'Простая швабра', 'images/mop.png', 'уборка'),
    ('Губка', 50, 'Универсальная губка', 'images/sponge.png', 'уборка'),
    ('Метла', 150, 'Садовая метла', 'images/broom.png', 'уборка'),
    ('Моющее средство', 300, 'Жидкое моющее средство', 'images/detergent.png', 'уборка'),
    ('Перчатки', 120, 'Хозяйственные перчатки', 'images/gloves.png', 'уборка'),
    ('Щётка', 80, 'Щётка для пола', 'images/brush.png', 'уборка'),
    ('Пакеты для мусора', 60, 'Упаковка пакетов 30л', 'images/trashbags.png', 'уборка'),
    ('Тряпка', 40, 'Микрофибровая тряпка', 'images/cloth.png', 'уборка'),
    ('Очиститель', 250, 'Средство для чистки кухни', 'images/cleaner.png', 'кухня')
]

cur.execute('DELETE FROM product')
cur.executemany(
    'INSERT INTO product (name, price, description, image, category) VALUES (?,?,?,?,?)',
    products
)

# ----- seed demo user -----
cur.execute('DELETE FROM user')
cur.execute(
    'INSERT INTO user (username, password) VALUES (?, ?)',
    ('admin', generate_password_hash('admin'))
)

conn.commit()
conn.close()
print('Database initialized with sample data.')

