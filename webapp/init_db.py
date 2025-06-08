import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    image TEXT
)''')

products = [
    ('Ведро', 100, 'Пластиковое ведро 10л', 'images/bucket.png'),
    ('Швабра', 200, 'Простая швабра', 'images/mop.png'),
    ('Губка', 50, 'Универсальная губка', 'images/sponge.png'),
    ('Метла', 150, 'Садовая метла', 'images/broom.png'),
    ('Моющее средство', 300, 'Жидкое моющее средство', 'images/detergent.png')
]

cur.execute('DELETE FROM product')
cur.executemany('INSERT INTO product (name, price, description, image) VALUES (?,?,?,?)', products)

conn.commit()
conn.close()
print('Database initialized with sample data.')

