import os
from flask import Flask, render_template_string, request, redirect, url_for, session
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

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - SaaS Inventory Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 text-gray-100 min-h-screen flex items-center justify-center font-sans p-4">
    <div class="max-w-md w-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 rounded-2xl p-8 shadow-2xl">
        <div class="text-center mb-6">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-emerald-600/25 border border-emerald-500/30 text-emerald-400 text-2xl mb-3 shadow-inner">⚡</div>
            <h1 class="text-2xl font-bold tracking-tight text-white">SaaS Inventory Hub</h1>
            <p class="text-xs text-slate-400 mt-1">សូមបញ្ចូលគណនីហាងរបស់អ្នកដើម្បីចូលកាន់ប្រព័ន្ធ</p>
        </div>
        {% if error %}
        <div class="bg-red-500/10 border border-red-500/30 text-red-400 text-xs p-3.5 rounded-xl mb-4 text-center">
            ⚠️ {{ error }}
        </div>
        {% endif %}
        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Username</label>
                <input type="text" name="username" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="ឈ្មោះអ្នកប្រើប្រាស់">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Password</label>
                <input type="password" name="password" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 rounded-xl shadow-lg transition text-sm">Login to Store</button>
        </form>
        <div class="text-center mt-5 text-xs text-slate-400">
            មិនទាន់មានហាងមែនទេ? <a href="/signup" class="text-emerald-400 font-semibold hover:underline">ចុះឈ្មោះហាងថ្មី (Sign Up)</a>
        </div>
    </div>
</body>
</html>
"""

SIGNUP_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up Store - SaaS Inventory Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 text-gray-100 min-h-screen flex items-center justify-center font-sans p-4">
    <div class="max-w-md w-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 rounded-2xl p-8 shadow-2xl">
        <div class="text-center mb-6">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-emerald-600/25 border border-emerald-500/30 text-emerald-400 text-2xl mb-3 shadow-inner">🏪</div>
            <h1 class="text-2xl font-bold tracking-tight text-white">Register New Store</h1>
            <p class="text-xs text-slate-400 mt-1">បង្កើតហាង និងគណនី Admin របស់អ្នកថ្មី</p>
        </div>
        {% if error %}
        <div class="bg-red-500/10 border border-red-500/30 text-red-400 text-xs p-3.5 rounded-xl mb-4 text-center">
            ⚠️ {{ error }}
        </div>
        {% endif %}
        <form action="/signup" method="POST" class="space-y-4">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Store Name (ឈ្មោះហាង)</label>
                <input type="text" name="store_name" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="ឧ. ហាងលក់ទំនិញ ABC">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Your Full Name (ឈ្មោះម្ចាស់ហាង)</label>
                <input type="text" name="admin_fullname" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="ឧ. សុខា">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Username (ឈ្មោះចូលប្រើ)</label>
                <input type="text" name="username" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="username">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Password (ពាក្យសម្ងាត់)</label>
                <input type="password" name="password" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 rounded-xl shadow-lg transition text-sm">Create Store & Account</button>
        </form>
        <div class="text-center mt-5 text-xs text-slate-400">
            មានគណនីរួចហើយ? <a href="/login" class="text-emerald-400 font-semibold hover:underline">ចូលគណនី (Login)</a>
        </div>
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Store Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-100 text-gray-800 min-h-screen font-sans">
    <div class="max-w-4xl mx-auto p-4 sm:p-6" x-data="{ tab: 'dashboard' }">
        <header class="bg-emerald-700 text-white rounded-lg p-3 sm:p-4 flex justify-between items-center mb-4 shadow-md">
            <div>
                <h1 class="text-base sm:text-lg font-bold">Store Dashboard</h1>
                <p class="text-xs text-emerald-200">Store ID: {{ store_id }}</p>
            </div>
            <div class="flex items-center space-x-2">
                <span class="text-xs bg-emerald-800 px-3 py-1.5 rounded">👤 {{ current_user }}</span>
                <a href="/logout" class="bg-red-500 hover:bg-red-600 text-white text-xs font-semibold px-3 py-1.5 rounded shadow">Logout</a>
            </div>
        </header>

        <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 mb-6 bg-white p-2 rounded-lg shadow-sm border border-gray-200">
            <button @click="tab = 'dashboard'" :class="tab === 'dashboard' ? 'bg-emerald-700 text-white' : 'bg-emerald-50 text-emerald-800'" class="px-3 py-2 rounded-md text-xs font-semibold text-center">Home</button>
            <button @click="tab = 'add'" :class="tab === 'add' ? 'bg-emerald-700 text-white' : 'bg-emerald-50 text-emerald-800'" class="px-3 py-2 rounded-md text-xs font-semibold text-center">Add Product</button>
            <button @click="tab = 'stock'" :class="tab === 'stock' ? 'bg-emerald-700 text-white' : 'bg-emerald-50 text-emerald-800'" class="px-3 py-2 rounded-md text-xs font-semibold text-center">Stock</button>
            <button @click="tab = 'sales'" :class="tab === 'sales' ? 'bg-emerald-700 text-white' : 'bg-emerald-50 text-emerald-800'" class="px-3 py-2 rounded-md text-xs font-semibold text-center">Sales</button>
            <button @click="tab = 'users'" :class="tab === 'users' ? 'bg-emerald-700 text-white' : 'bg-emerald-50 text-emerald-800'" class="px-3 py-2 rounded-md text-xs font-semibold text-center">Users</button>
        </div>

        <div x-show="tab === 'dashboard'" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white border p-4 rounded-lg shadow-sm"><p class="text-xs text-gray-500">Total Items</p><p class="text-2xl font-bold mt-1">{{ total_items }}</p></div>
                <div class="bg-white border p-4 rounded-lg shadow-sm"><p class="text-xs text-gray-500">Total Stock Qty</p><p class="text-2xl font-bold mt-1">{{ total_stock }}</p></div>
                <div class="bg-white border p-4 rounded-lg shadow-sm"><p class="text-xs text-gray-500">Inventory Asset Value</p><p class="text-2xl font-bold text-emerald-600 mt-1">${{ "%.2f"|format(inventory_value) }}</p></div>
            </div>
        </div>

        <div x-show="tab === 'add'" class="bg-white border rounded-lg p-5 shadow-sm" style="display: none;">
            <h2 class="text-sm font-bold text-gray-700 mb-4 uppercase">Add New Product</h2>
            <form action="/add" method="POST" class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div><label class="block text-xs font-medium text-gray-600 mb-1">Product Name</label><input type="text" name="name" required class="w-full border rounded-md px-3 py-2 text-sm"></div>
                    <div><label class="block text-xs font-medium text-gray-600 mb-1">Price ($)</label><input type="number" step="0.01" name="price" required class="w-full border rounded-md px-3 py-2 text-sm"></div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div><label class="block text-xs font-medium text-gray-600 mb-1">Category</label><input type="text" name="category" class="w-full border rounded-md px-3 py-2 text-sm" value="General"></div>
                    <div><label class="block text-xs font-medium text-gray-600 mb-1">Initial Stock</label><input type="number" name="stock" required class="w-full border rounded-md px-3 py-2 text-sm"></div>
                </div>
                <button type="submit" class="w-full bg-emerald-700 hover:bg-emerald-800 text-white font-semibold py-2.5 rounded-md text-sm">Save Product</button>
            </form>
        </div>

        <div x-show="tab === 'stock'" class="bg-white border rounded-lg p-5 shadow-sm" style="display: none;">
            <h2 class="text-sm font-bold text-gray-700 mb-4 uppercase">Stock Management</h2>
            <table class="w-full text-left border-collapse">
                <thead><tr class="border-b text-xs text-gray-500 uppercase"><th class="p-3">Name</th><th class="p-3">Category</th><th class="p-3">Price</th><th class="p-3">Stock</th></tr></thead>
                <tbody class="divide-y text-sm">
                    {% for p in products %}
                    <tr><td class="p-3">{{ p.name }}</td><td class="p-3">{{ p.category }}</td><td class="p-3">${{ "%.2f"|format(p.price) }}</td><td class="p-3">{{ p.stock }}</td></tr>
                    {% else %}
                    <tr><td colspan="4" class="p-6 text-center text-gray-400 italic">មិនមានទំនិញក្នុងស្តុកទេ។</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div x-show="tab === 'sales'" class="bg-white border rounded-lg p-5 shadow-sm" style="display: none;"><p class="text-sm text-gray-500 italic text-center">មិនទាន់មានប្រវត្តិការលក់។</p></div>

        <div x-show="tab === 'users'" class="bg-white border rounded-lg p-5 shadow-sm space-y-3" style="display: none;">
            <h2 class="text-sm font-bold text-gray-700 mb-4 uppercase">Store Users</h2>
            {% for u in users_list %}
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-md border"><p class="text-sm font-semibold">{{ u.name }} ({{ u.username }})</p><span class="text-xs bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full">{{ u.role }}</span></div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

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
            session['role'] = user.get('role', 'Admin')
            return redirect(url_for("index"))
        else:
            error = "ឈ្មោះអ្នកប្រើប្រាស់ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        store_name = request.form.get("store_name")
        admin_fullname = request.form.get("admin_fullname")
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = supabase_request(f"users?username=eq.{username}&select=*")
        if existing_user and len(existing_user) > 0:
            error = "ឈ្មោះ Username នេះមានគេប្រើរួចហើយ សូមជ្រើសរើសផ្សេង!"
            return render_template_string(SIGNUP_TEMPLATE, error=error)

        new_store_data = {"name": store_name}
        created_stores = supabase_request("stores", method="POST", data=new_store_data)
        
        if not created_stores or len(created_stores) == 0:
            error = "មានបញ្ហាពេលបង្កើតហាង សូមព្យាយាមម្ដងទៀត!"
            return render_template_string(SIGNUP_TEMPLATE, error=error)
            
        new_store_id = created_stores[0]["id"]

        new_user_data = {
            "store_id": new_store_id,
            "name": admin_fullname,
            "username": username,
            "password": password,
            "role": "Admin"
        }
        created_users = supabase_request("users", method="POST", data=new_user_data)

        if not created_users or len(created_users) == 0:
            error = "បង្កើតហាងបានហើយ ប៉ុន្តែមានបញ្ហាពេលបង្កើតគណនី Admin!"
            return render_template_string(SIGNUP_TEMPLATE, error=error)

        user = created_users[0]
        session['user'] = user['name']
        session['store_id'] = user['store_id']
        session['role'] = user.get('role', 'Admin')
        return redirect(url_for("index"))

    return render_template_string(SIGNUP_TEMPLATE, error=error)

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
    if not isinstance(products, list): products = []
    users_list = supabase_request(f"users?store_id=eq.{current_store_id}&select=*")
    if not isinstance(users_list, list): users_list = []
    
    total_items = len(products)
    total_stock = sum(int(p.get("stock", 0) or 0) for p in products)
    inventory_value = sum(float(p.get("price", 0) or 0) * int(p.get("stock", 0) or 0) for p in products)
    
    return render_template_string(INDEX_TEMPLATE, 
                           products=products, 
                           users_list=users_list,
                           total_items=total_items, 
                           total_stock=total_stock, 
                           inventory_value=inventory_value,
                           current_user=session.get('user'),
                           store_id=current_store_id)

@app.route("/add", methods=["POST"])
def add_product():
    if 'user' not in session: return redirect(url_for("login"))
    new_product = {
        "store_id": session.get('store_id'),
        "name": request.form.get("name"),
        "category": request.form.get("category") or "General",
        "price": float(request.form.get("price") or 0.0),
        "stock": int(request.form.get("stock") or 0)
    }
    supabase_request("products", method="POST", data=new_product)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
