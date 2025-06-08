from flask import Flask, render_template, abort
import sqlite3

app = Flask(__name__)
DB_PATH = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM product').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM product WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not product:
        abort(404)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)

