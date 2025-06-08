from flask import Flask, render_template, abort

app = Flask(__name__)

# Простейшие данные о товарах
products = [
    {"id": 1, "name": "Ведро", "price": 100, "description": "Пластиковое ведро 10л"},
    {"id": 2, "name": "Швабра", "price": 200, "description": "Простая швабра"},
    {"id": 3, "name": "Губка", "price": 50, "description": "Универсальная губка"},
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        abort(404)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
