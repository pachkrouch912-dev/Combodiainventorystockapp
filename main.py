import os
from flask import Flask, render_template, request, redirect, url_for, session
import urllib.request
import json

app = Flask(__name__)
app.secret_key = "cambodia-inventory-secure-secret-key"

SUPABASE_URL = "https://dwqyrlrylworstasglsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3cXlybHJ5bHdvcnN0YXNnbsiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTc4NTUwNTc3MCwiZXhwIjoyMTAxMDgxNzcwfQ.BjfkTVs-BOkl8gdCvX4rEuN8N4L8Y3KQkzRxmGipR1U"

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

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        users = supabase_request(f"users?username=eq.{username}&password=eq.{password}&select=*")
        
        if users and len(users) > 0:
            user = users[0]
            session['user'] = user['name']
            session['store_id'] = user['store_id']
            session['role'] = user.get('role', 'Staff')
            return redirect(url_for("index"))
        else:
            error = "ឈ្មោះអ្នកប្រើប្រាស់ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"
            
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    if 'user' not in session:
        return redirect(url_for("login"))
        
    current_store_id = session.get('store_id')
    
    products = supabase_request(f"products?store_id=eq.{current_store_id}&select=*")
    if not isinstance(products, list):
        products = []
        
    users_list = supabase_request(f"users?store_id=eq.{current_store_id}&select=*")
    if not isinstance(users_list, list):
        users_list = []
        
    total_items = len(products)
    total_stock = sum(int(p.get("stock", 0) or 0) for p in products)
    inventory_value = sum(float(p.get("price", 0) or 0) * int(p.get("stock", 0) or 0) for p in products)
    
    return render_template("index.html", 
                           products=products, 
                           users_list=users_list,
                           total_items=total_items, 
                           total_stock=total_stock, 
                           inventory_value=inventory_value,
                           current_user=session.get('user'))

@app.route("/add", methods=["POST"])
def add_product():
    if 'user' not in session:
        return redirect(url_for("login"))
        
    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    stock = request.form.get("stock")
    
    new_product = {
        "store_id": session.get('store_id'),
        "name": name,
        "category": category if category else "General",
        "price": float(price) if price else 0.0,
        "stock": int(stock) if stock else 0
    }
    
    supabase_request("products", method="POST", data=new_product)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
