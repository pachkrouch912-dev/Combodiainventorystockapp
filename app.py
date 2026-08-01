import os
from flask import Flask, render_template_string, request, redirect, url_for, session
import urllib.request
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cambodia-inventory-secure-secret-key"

SUPABASE_URL = "https://dwqyrlrylworstasglsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3cXlybHJ5bHdvcnN0YXNnbHNpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTUwNTc3MCwiZXhwIjoyMTAxMDgxNzcwfQ.gR5rqaHs44_4pH-ufkdRRhsx1rt2jEAnP1d905Go5Rc"

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

AUTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Inventory Hub - Authentication</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 text-gray-100 min-h-screen flex items-center justify-center font-sans p-4">
    <div class="max-w-md w-full bg-slate-900/90 backdrop-blur-xl border border-slate-700/60 rounded-3xl p-8 shadow-2xl shadow-emerald-950/50" x-data="{ mode: '{{ mode|default('login') }}' }">
        <div class="text-center mb-6">
            <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 text-white text-2xl mb-3 shadow-lg shadow-emerald-600/30">⚡</div>
            <h1 class="text-2xl font-extrabold tracking-tight text-white">SaaS Inventory Hub</h1>
            <p class="text-xs text-slate-400 mt-1.5" x-text="mode === 'login' ? 'សូមបញ្ចូលគណនីហាងរបស់អ្នកដើម្បីចូលកាន់ប្រព័ន្ធ' : 'បង្កើតហាង និងគណនី Admin របស់អ្នកថ្មី'"></p>
        </div>

        {% if error %}
        <div class="bg-red-500/10 border border-red-500/30 text-red-400 text-xs p-3.5 rounded-2xl mb-4 text-center font-medium">
            ⚠️ {{ error }}
        </div>
        {% endif %}

        <div class="grid grid-cols-2 gap-1.5 bg-slate-950/80 p-1.5 rounded-2xl mb-6 border border-slate-800/80">
            <button @click="mode = 'login'" :class="mode === 'login' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-400 hover:text-white'" class="py-2.5 text-xs font-bold rounded-xl transition-all duration-200">ចូលគណនី (Login)</button>
            <button @click="mode = 'signup'" :class="mode === 'signup' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-400 hover:text-white'" class="py-2.5 text-xs font-bold rounded-xl transition-all duration-200">ចុះឈ្មោះហាង (Sign Up)</button>
        </div>

        <form action="/login" method="POST" class="space-y-4" x-show="mode === 'login'">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Username</label>
                <input type="text" name="username" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="ឈ្មោះអ្នកប្រើប្រាស់">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Password</label>
                <input type="password" name="password" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold py-3 rounded-2xl shadow-lg shadow-emerald-600/30 transition-all text-sm mt-2">Login to Store</button>
        </form>

        <form action="/signup" method="POST" class="space-y-4" x-show="mode === 'signup'" style="display: none;">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Store Name (ឈ្មោះហាង)</label>
                <input type="text" name="store_name" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="ឧ. ហាងលក់ទំនិញ ABC">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Your Full Name (ឈ្មោះម្ចាស់ហាង)</label>
                <input type="text" name="admin_fullname" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="ឧ. សុខា">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Username (ឈ្មោះចូលប្រើ)</label>
                <input type="text" name="username" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="username">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Password (ពាក្យសម្ងាត់)</label>
                <input type="password" name="password" required class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold py-3 rounded-2xl shadow-lg shadow-emerald-600/30 transition-all text-sm mt-2">Create Store & Account</button>
        </form>
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
    <title>Store Dashboard - SaaS Inventory Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    <div class="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8" x-data="{ tab: 'dashboard' }">
        
        <!-- HEADER -->
        <header class="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white rounded-3xl p-5 sm:p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 shadow-xl shadow-emerald-950/40 border border-emerald-600/30 gap-4">
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-2xl shadow-inner">🏪</div>
                <div>
                    <h1 class="text-lg sm:text-xl font-black tracking-tight">Store Dashboard</h1>
                    <p class="text-xs text-emerald-200/90 font-medium mt-0.5">Store ID: <span class="bg-emerald-950/40 px-2 py-0.5 rounded-lg text-emerald-300 font-bold">#{{ store_id }}</span></p>
                </div>
            </div>
            <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end border-t sm:border-t-0 pt-3 sm:pt-0 border-emerald-600/40">
                <span class="text-xs bg-emerald-950/60 backdrop-blur-md px-3.5 py-2 rounded-2xl border border-emerald-500/20 font-semibold flex items-center space-x-1.5 shadow-sm">
                    <span>👤</span> <span class="text-emerald-100">{{ current_user }}</span>
                </span>
                <a href="/logout" class="bg-rose-500/90 hover:bg-rose-600 text-white text-xs font-bold px-4 py-2 rounded-2xl shadow-lg shadow-rose-900/40 transition-all flex items-center space-x-1">Logout</a>
            </div>
        </header>

        <!-- NAVIGATION TABS -->
        <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 mb-6 bg-slate-800/80 backdrop-blur-xl p-2 rounded-2xl shadow-lg border border-slate-700/60">
            <button @click="tab = 'dashboard'" :class="tab === 'dashboard' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">Home</button>
            <button @click="tab = 'pos'" :class="tab === 'pos' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">POS Sell</button>
            <button @click="tab = 'add'" :class="tab === 'add' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">Add Item</button>
            <button @click="tab = 'stock'" :class="tab === 'stock' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">Stock</button>
            <button @click="tab = 'sales'" :class="tab === 'sales' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">Sales</button>
            <button @click="tab = 'logs'" :class="tab === 'logs' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'" class="px-3 py-2.5 rounded-xl text-xs font-bold transition-all text-center">Movement</button>
        </div>

        <!-- HOME DASHBOARD -->
        <div x-show="tab === 'dashboard'" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 p-5 rounded-3xl shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Items</p>
                    <p class="text-3xl font-black text-white mt-2">{{ total_items }}</p>
                </div>
                <div class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 p-5 rounded-3xl shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Stock Qty</p>
                    <p class="text-3xl font-black text-white mt-2">{{ total_stock }}</p>
                </div>
                <div class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 p-5 rounded-3xl shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Inventory Asset Value</p>
                    <p class="text-3xl font-black text-emerald-400 mt-2">${{ "%.2f"|format(inventory_value) }}</p>
                </div>
            </div>
        </div>

        <!-- POS SELL TAB -->
        <div x-show="tab === 'pos'" class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 rounded-3xl p-6 shadow-xl" style="display: none;">
            <h2 class="text-sm font-black text-white mb-5 uppercase tracking-wider flex items-center space-x-2"><span>⚡ POS - លក់ទំនិញ (Checkout)</span></h2>
            <form action="/sell" method="POST" class="space-y-5 max-w-lg">
                <div>
                    <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">ជ្រើសរើសទំនិញ (Select Product)</label>
                    <select name="product_id" required class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all">
                        <option value="">-- ជ្រើសរើសទំនិញ --</option>
                        {% for p in products %}
                        <option value="{{ p.id }}">{{ p.name }} (សល់: {{ p.stock }} | ${{ "%.2f"|format(p.price) }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">ចំនួនលក់ (Quantity)</label>
                    <input type="number" name="quantity" min="1" value="1" required class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold py-3.5 rounded-2xl shadow-lg shadow-emerald-600/30 transition-all text-sm">គិតលុយ និងកាត់ស្តុក (Confirm Sale)</button>
            </form>
        </div>

        <!-- ADD PRODUCT TAB -->
        <div x-show="tab === 'add'" class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 rounded-3xl p-6 shadow-xl" style="display: none;">
            <h2 class="text-sm font-black text-white mb-5 uppercase tracking-wider flex items-center space-x-2"><span>📦 Add New Product</span></h2>
            <form action="/add" method="POST" class="space-y-4 max-w-xl">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div><label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Product Name</label><input type="text" name="name" required class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500"></div>
                    <div><label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Price ($)</label><input type="number" step="0.01" name="price" required class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500"></div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div><label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Category</label><input type="text" name="category" class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500" value="General"></div>
                    <div><label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Initial Stock</label><input type="number" name="stock" required class="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500"></div>
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold py-3.5 rounded-2xl shadow-lg shadow-emerald-600/30 transition-all text-sm mt-2">Save Product</button>
            </form>
        </div>

        <!-- STOCK MANAGEMENT TAB -->
        <div x-show="tab === 'stock'" class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 rounded-3xl p-6 shadow-xl overflow-hidden" style="display: none;">
            <h2 class="text-sm font-black text-white mb-5 uppercase tracking-wider">Stock Management</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead><tr class="border-b border-slate-700 text-xs text-slate-400 uppercase tracking-wider"><th class="p-3.5">Name</th><th class="p-3.5">Category</th><th class="p-3.5">Price</th><th class="p-3.5">Stock</th></tr></thead>
                    <tbody class="divide-y divide-slate-700/50 text-sm">
                        {% for p in products %}
                        <tr class="hover:bg-slate-700/30 transition-colors"><td class="p-3.5 font-semibold text-white">{{ p.name }}</td><td class="p-3.5 text-slate-300"><span class="bg-slate-900 px-2.5 py-1 rounded-xl text-xs border border-slate-700">{{ p.category }}</span></td><td class="p-3.5 text-emerald-400 font-bold">${{ "%.2f"|format(p.price) }}</td><td class="p-3.5 font-black text-white">{{ p.stock }}</td></tr>
                        {% else %}
                        <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនមានទំនិញក្នុងស្តុកទេ។</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SALES HISTORY TAB -->
        <div x-show="tab === 'sales'" class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 rounded-3xl p-6 shadow-xl overflow-hidden" style="display: none;">
            <h2 class="text-sm font-black text-white mb-5 uppercase tracking-wider">Sales History (ប្រវត្តិការលក់)</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead><tr class="border-b border-slate-700 text-xs text-slate-400 uppercase tracking-wider"><th class="p-3.5">Product</th><th class="p-3.5">Qty</th><th class="p-3.5">Total ($)</th><th class="p-3.5">Date</th></tr></thead>
                    <tbody class="divide-y divide-slate-700/50 text-sm">
                        {% for s in sales_list %}
                        <tr class="hover:bg-slate-700/30 transition-colors"><td class="p-3.5 font-semibold text-white">{{ s.product_name }}</td><td class="p-3.5 font-bold text-white">{{ s.quantity }}</td><td class="p-3.5 text-emerald-400 font-black">${{ "%.2f"|format(s.total_price) }}</td><td class="p-3.5 text-xs text-slate-400">{{ s.created_at }}</td></tr>
                        {% else %}
                        <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនទាន់មានប្រវត្តិការលក់។</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- STOCK MOVEMENT TAB -->
        <div x-show="tab === 'logs'" class="bg-slate-800/90 backdrop-blur-xl border border-slate-700/70 rounded-3xl p-6 shadow-xl overflow-hidden" style="display: none;">
            <h2 class="text-sm font-black text-white mb-5 uppercase tracking-wider">Stock Movement (ប្រវត្តិបម្រែបម្រួលស្តុក)</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead><tr class="border-b border-slate-700 text-xs text-slate-400 uppercase tracking-wider"><th class="p-3.5">Type</th><th class="p-3.5">Details</th><th class="p-3.5">Qty Change</th><th class="p-3.5">Date</th></tr></thead>
                    <tbody class="divide-y divide-slate-700/50 text-sm">
                        {% for m in movements %}
                        <tr class="hover:bg-slate-700/30 transition-colors">
                            <td class="p-3.5"><span class="px-2.5 py-1 text-xs font-bold rounded-xl {{ 'bg-rose-500/10 text-rose-400 border border-rose-500/30' if m.type == 'OUT' else 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' }}">{{ m.type }}</span></td>
                            <td class="p-3.5 font-medium text-slate-200">{{ m.description }}</td>
                            <td class="p-3.5 font-black {{ 'text-rose-400' if m.type == 'OUT' else 'text-emerald-400' }}">{{ m.qty_change }}</td>
                            <td class="p-3.5 text-xs text-slate-400">{{ m.created_at }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនទាន់មានទិន្នន័យ Stock Movement.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def auth_page():
    if 'user' in session:
        return redirect(url_for("index"))
    return render_template_string(AUTH_TEMPLATE, mode="login", error=None)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    users = supabase_request(f"users?username=eq.{username}&password=eq.{password}&select=*")
    if users and len(users) > 0:
        user = users[0]
        session['user'] = user['name']
        session['store_id'] = user['store_id']
        session['role'] = user.get('role', 'Admin')
        return redirect(url_for("index"))
    return render_template_string(AUTH_TEMPLATE, mode="login", error="ឈ្មោះអ្នកប្រើប្រាស់ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ!")

@app.route("/signup", methods=["POST"])
def signup():
    store_name = request.form.get("store_name")
    admin_fullname = request.form.get("admin_fullname")
    username = request.form.get("username")
    password = request.form.get("password")

    existing_user = supabase_request(f"users?username=eq.{username}&select=*")
    if existing_user and len(existing_user) > 0:
        return render_template_string(AUTH_TEMPLATE, mode="signup", error="ឈ្មោះ Username នេះមានគេប្រើរួចហើយ!")

    created_stores = supabase_request("stores", method="POST", data={"name": store_name})
    if not created_stores:
        return render_template_string(AUTH_TEMPLATE, mode="signup", error="មានបញ្ហាពេលបង្កើតហាង សូមព្យាយាមម្ដងទៀត!")
        
    new_store_id = created_stores[0]["id"]
    created_users = supabase_request("users", method="POST", data={
        "store_id": new_store_id,
        "name": admin_fullname,
        "username": username,
        "password": password,
        "role": "Admin"
    })

    if not created_users:
        return render_template_string(AUTH_TEMPLATE, mode="signup", error="មានបញ្ហាពេលបង្កើតគណនី Admin!")

    user = created_users[0]
    session['user'] = user['name']
    session['store_id'] = user['store_id']
    session['role'] = user.get('role', 'Admin')
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_page"))

@app.route("/dashboard")
def index():
    if 'user' not in session:
        return redirect(url_for("auth_page"))
        
    current_store_id = session.get('store_id')
    products = supabase_request(f"products?store_id=eq.{current_store_id}&select=*")
    if not isinstance(products, list): products = []
    
    sales_list = supabase_request(f"sales?store_id=eq.{current_store_id}&select=*")
    if not isinstance(sales_list, list): sales_list = []

    movements = supabase_request(f"stock_movements?store_id=eq.{current_store_id}&select=*")
    if not isinstance(movements, list): movements = []
    
    total_items = len(products)
    total_stock = sum(int(p.get("stock", 0) or 0) for p in products)
    inventory_value = sum(float(p.get("price", 0) or 0) * int(p.get("stock", 0) or 0) for p in products)
    
    return render_template_string(INDEX_TEMPLATE, 
                           products=products, 
                           sales_list=sales_list,
                           movements=movements,
                           total_items=total_items, 
                           total_stock=total_stock, 
                           inventory_value=inventory_value,
                           current_user=session.get('user'),
                           store_id=current_store_id)

@app.route("/add", methods=["POST"])
def add_product():
    if 'user' not in session: return redirect(url_for("auth_page"))
    store_id = session.get('store_id')
    name = request.form.get("name")
    stock_qty = int(request.form.get("stock") or 0)
    
    prod_res = supabase_request("products", method="POST", data={
        "store_id": store_id,
        "name": name,
        "category": request.form.get("category") or "General",
        "price": float(request.form.get("price") or 0.0),
        "stock": stock_qty
    })
    
    if prod_res:
        supabase_request("stock_movements", method="POST", data={
            "store_id": store_id,
            "type": "IN",
            "description": f"Added product: {name}",
            "qty_change": stock_qty
        })
        
    return redirect(url_for("index"))

@app.route("/sell", methods=["POST"])
def sell_product():
    if 'user' not in session: return redirect(url_for("auth_page"))
    store_id = session.get('store_id')
    product_id = request.form.get("product_id")
    qty = int(request.form.get("quantity") or 1)
    
    products = supabase_request(f"products?id=eq.{product_id}&select=*")
    if not products: return redirect(url_for("index"))
    product = products[0]
    
    current_stock = int(product.get("stock", 0))
    if current_stock < qty:
        return redirect(url_for("index"))
        
    new_stock = current_stock - qty
    total_price = float(product.get("price", 0)) * qty
    
    urllib.request.urlopen(urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}",
        data=json.dumps({"stock": new_stock}).encode("utf-8"),
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"},
        method="PATCH"
    ))
    
    supabase_request("sales", method="POST", data={
        "store_id": store_id,
        "product_name": product['name'],
        "quantity": qty,
        "total_price": total_price
    })
    
    supabase_request("stock_movements", method="POST", data={
        "store_id": store_id,
        "type": "OUT",
        "description": f"Sold: {product['name']}",
        "qty_change": -qty
    })
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

