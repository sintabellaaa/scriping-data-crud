# web_scraper.py
import requests
import json
import csv

url = "https://fakestoreapi.com/products"
response = requests.get(url)

if response.status_code == 200:
    products = response.json()

    data = []

    # Tambahkan id otomatis
    for idx, product in enumerate(products, start=1):
        title = product["title"]
        price = product["price"]
        category = product["category"]

        data.append({
            "id": idx,
            "Produk": title,
            "Harga": price,
            "Kategori": category
        })

    # --- Simpan ke file JSON ---
    with open("products.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print("Data berhasil disimpan ke products.json")

    # --- Simpan ke file CSV ---
    with open("products.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "Produk", "Harga", "Kategori"])
        writer.writeheader()
        writer.writerows(data)
    print("Data berhasil disimpan ke products.csv")

else:
    print("Gagal mengakses API.")