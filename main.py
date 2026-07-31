import os
from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request
import json

app = Flask(__name__)
app.secret_key = "cambodia-inventory-secret-key"

# ភ្ជាប់ដោយផ្ទាល់ជាមួយ Supabase Project របស់បង
SUPABASE_URL = "https://dwqyrlrylworstasglsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3cXlybHJ5bHdvcnN0YXNnbHNpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU1MDU3NzAsImV4cCI6MjEwMTA4MTc3MH0.BjfkTVs-BOkl8gdCvX4rEuN8N4L8Y3KQkzRxmGipR1U"

def supabase_request(endpoint, method="GET", data=None):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else []
    except Exception as e:
        print(f"Supabase Error: {e}")
        return []

@app.route("/")
def index():
    # ទាញទិន្នន័យពីតារាង products ក្នុង Supabase
    products = supabase_request("products?select=*")
    if not isinstance(products, list):
        products = []
        
    total_items = len(products)
    total_stock = sum(int(p.get("stock", 0) or 0) for p in products)
    inventory_value = sum(float(p.get("price", 0) or 0) * int(p.get("stock", 0) or 0) for p in products)
    
    return render_template("index.html", 
                           products=products, 
                           total_items=total_items, 
                           total_stock=total_stock, 
                           inventory_value=inventory_value)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    stock = request.form.get("stock")
    
    new_product = {
        "name": name,
        "category": category,
        "price": float(price) if price else 0.0,
        "stock": int(stock) if stock else 0
    }
    
    supabase_request("products", method="POST", data=new_product)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
