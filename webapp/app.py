from flask import (
    Flask, render_template, abort, request,
    redirect, url_for, session, flash, g
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev-secret'
DB_PATH = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Нужно войти в аккаунт')
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return wrapped


@app.before_request
def load_categories():
    conn = get_db_connection()
    g.categories = conn.execute('SELECT DISTINCT category FROM product').fetchall()
    conn.close()

@app.route('/')
def index():
    category = request.args.get('category')
    query = request.args.get('q', '')

    conn = get_db_connection()
    sql = 'SELECT * FROM product WHERE 1=1'
    params = []
    if category:
        sql += ' AND category = ?'
        params.append(category)
    if query:
        sql += ' AND name LIKE ?'
        params.append(f'%{query}%')

    products = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template('index.html', products=products,
                           current_category=category, query=query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM product WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not product:
        abort(404)
    return render_template('product.html', product=product)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Введите имя пользователя и пароль')
        else:
            conn = get_db_connection()
            try:
                conn.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                conn.commit()
                flash('Регистрация прошла успешно')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Пользователь уже существует')
            finally:
                conn.close()
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            flash('Вход выполнен')
            return redirect(url_for('index'))
        flash('Неверные имя пользователя или пароль')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('index'))


@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = session.setdefault('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    flash('Товар добавлен в корзину')
    return redirect(request.referrer or url_for('index'))


@app.route('/cart')
@login_required
def cart():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        products = []
    else:
        placeholders = ','.join('?' for _ in cart_ids)
        conn = get_db_connection()
        products = conn.execute(
            f'SELECT * FROM product WHERE id IN ({placeholders})', cart_ids
        ).fetchall()
        conn.close()
    return render_template('cart.html', products=products)


@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        flash('Корзина пуста')
        return redirect(url_for('index'))
    conn = get_db_connection()
    placeholders = ','.join('?' for _ in cart_ids)
    products = conn.execute(
        f'SELECT * FROM product WHERE id IN ({placeholders})', cart_ids
    ).fetchall()
    conn.close()
    if request.method == 'POST':
        session.pop('cart', None)
        flash('Заказ оформлен!')
        return redirect(url_for('index'))
    return render_template('order.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)

