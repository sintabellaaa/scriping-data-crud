from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Fungsi untuk baca data dari JSON
def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Fungsi untuk simpan data ke JSON
def save_products(products):
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

# --- READ semua produk ---
@app.route("/products", methods=["GET"])
def get_products():
    products = load_products()
    return jsonify(products)

# --- READ produk berdasarkan id ---
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    return jsonify(product) if product else ("Not Found", 404)

# --- CREATE produk baru ---
@app.route("/products", methods=["POST"])
def add_product():
    products = load_products()
    new_product = request.json
    new_product["id"] = max(p["id"] for p in products) + 1  # id otomatis
    products.append(new_product)
    save_products(products)
    return jsonify(new_product), 201

# --- UPDATE produk berdasarkan id ---
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product.update(request.json)
        save_products(products)
        return jsonify(product)
    return ("Not Found", 404)

# --- DELETE produk berdasarkan id ---
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        products = [p for p in products if p["id"] != product_id]
        save_products(products)
        return jsonify({"message": "Deleted", "product": product}), 200
    return ("Not Found", 404)

if __name__ == "__main__":
    app.run(debug=True)