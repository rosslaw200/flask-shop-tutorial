from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        total REAL,
        status TEXT DEFAULT 'Pending'
    )
    """)

    db.commit()

    # Seed mock products
    count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        mock_products = [
            ('Organic Tomatoes (1kg)', 4.99, 50),
            ('Fresh Strawberries (500g)', 3.50, 30),
            ('Raw Local Honey (Jar)', 8.00, 20),
            ('Free-range Eggs (Dozen)', 5.50, 40)
        ]
        db.executemany("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", mock_products)
        db.commit()

    # Seed admin user
    admin_email = 'admin@admin.com'
    admin_pass = 'admin123'
    existing_admin = db.execute("SELECT * FROM users WHERE email=?", (admin_email,)).fetchone()
    if not existing_admin:
        db.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (admin_email, admin_pass, 'admin')
        )
        db.commit()

    # Migration: Add status column if it doesn't exist
    try:
        db.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'Pending'")
        db.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass


def get_db():
    return sqlite3.connect("database.db")

# Home
@app.route("/")
def index():
    db = get_db()
    featured_products = db.execute("SELECT * FROM products LIMIT 4").fetchall()
    return render_template("index.html", products=featured_products)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[3]
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        existing = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            return "Email already registered"

        db.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, password, 'user')
        )
        db.commit()

        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        session["user_id"] = user[0]
        session["role"] = user[3]
        return redirect("/")

    return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Catalogue
@app.route("/catalogue")
def catalogue():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("catalogue.html", products=products)

# Product page
@app.route("/product/<int:id>")
def product(id):
    db = get_db()
    product = db.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("product.html", product=product)

# Search
@app.route("/search")
def search():
    keyword = request.args.get("q")

    db = get_db()
    products = db.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        ("%" + keyword + "%",)
    ).fetchall()

    return render_template("catalogue.html", products=products)

# Order
@app.route("/order", methods=["POST"])
def order():
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    db = get_db()

    product = db.execute(
        "SELECT stock, price FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    if product:
        stock = product[0]
        price = product[1]

        if quantity > 0 and stock >= quantity:
            total = price * quantity

            db.execute(
                "INSERT INTO orders (product_id, quantity, total) VALUES (?, ?, ?)",
                (product_id, quantity, total)
            )

            db.execute(
                "UPDATE products SET stock = stock - ? WHERE id=?",
                (quantity, product_id)
            )

            db.commit()

            return "Order placed successfully"
        else:
            return "Invalid quantity or not enough stock"
    else:
        return "Product not found"

# Producer Dashboard
@app.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    orders = db.execute("""
        SELECT orders.id, products.name, orders.quantity, orders.total, orders.status 
        FROM orders 
        JOIN products ON orders.product_id = products.id
    """).fetchall()

    return render_template("dashboard.html", products=products, orders=orders)

# Admin: Add Product
@app.route("/admin/product/add", methods=["POST"])
def add_product():
    if session.get("role") != "admin":
        return redirect("/login")
    
    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    
    db = get_db()
    db.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    db.commit()
    return redirect("/dashboard")

# Admin: Update Product
@app.route("/admin/product/update", methods=["POST"])
def update_product():
    if session.get("role") != "admin":
        return redirect("/login")
    
    product_id = request.form["product_id"]
    name = request.form["name"]
    price = float(request.form["price"])
    
    db = get_db()
    db.execute("UPDATE products SET name=?, price=? WHERE id=?", (name, price, product_id))
    db.commit()
    return redirect("/dashboard")

# Admin: Add Stock
@app.route("/admin/product/add_stock", methods=["POST"])
def add_stock():
    if session.get("role") != "admin":
        return redirect("/login")
    
    product_id = request.form["product_id"]
    stock_to_add = int(request.form["stock"])
    
    db = get_db()
    db.execute("UPDATE products SET stock = stock + ? WHERE id=?", (stock_to_add, product_id))
    db.commit()
    return redirect("/dashboard")

# Admin: Delete Product
@app.route("/admin/product/delete", methods=["POST"])
def delete_product():
    if session.get("role") != "admin":
        return redirect("/login")
    
    product_id = request.form["product_id"]
    
    db = get_db()
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    return redirect("/dashboard")

# Admin: Update Order Status
@app.route("/admin/order/update_status", methods=["POST"])
def update_order_status():
    if session.get("role") != "admin":
        return redirect("/login")
    
    order_id = request.form["order_id"]
    new_status = request.form["status"]
    
    db = get_db()
    db.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    db.commit()
    return redirect("/dashboard")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)