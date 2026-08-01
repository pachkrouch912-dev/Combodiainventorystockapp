import os
from flask import Flask, render_template_string, request, redirect, url_for, session
import urllib.request
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cambodia-inventory-secure-secret-key"

SUPABASE_URL = "https://dwqyrlrylworstasglsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3cXlybHJ5bHdvcnN0YXNnbHNpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTUwNTc3MCwiZXhwIjoyMTAxMDgxNzcwfQ.gR5rqaHs44_4pH-ufkdRRhsx1rt2jEAnP1d905Go5Rc" # (ប្រើ key ដើមរបស់បង)

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
    <div class="max-w-md w-full bg-slate-900/95 backdrop-blur-xl border border-slate-700/60 rounded-2xl p-8 shadow-2xl" x-data="{ mode: '{{ mode|default('login') }}' }">
        <div class="text-center mb-6">
            <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-emerald-600/20 border border-emerald-500/30 text-emerald-400 text-3xl mb-3 shadow-inner">⚡</div>
            <h1 class="text-2xl font-bold tracking-tight text-white">SaaS Inventory Hub</h1>
            <p class="text-xs text-slate-400 mt-1" x-text="mode === 'login' ? 'សូមបញ្ចូលគណនីហាងរបស់អ្នកដើម្បីចូលកាន់ប្រព័ន្ធ' : 'បង្កើតហាង និងគណនី Admin របស់អ្នកថ្មី'"></p>
        </div>

        {% if error %}
        <div class="bg-red-500/10 border border-red-500/30 text-red-400 text-xs p-3.5 rounded-xl mb-4 text-center">
            ⚠️ {{ error }}
        </div>
        {% endif %}

        <div class="grid grid-cols-2 gap-1 bg-slate-950 p-1 rounded-xl mb-6 border border-slate-800">
            <button @click="mode = 'login'" :class="mode === 'login' ? 'bg-emerald-600 text-white shadow' : 'text-slate-400 hover:text-white'" class="py-2.5 text-xs font-semibold rounded-lg transition">ចូលគណនី (Login)</button>
            <button @click="mode = 'signup'" :class="mode === 'signup' ? 'bg-emerald-600 text-white shadow' : 'text-slate-400 hover:text-white'" class="py-2.5 text-xs font-semibold rounded-lg transition">ចុះឈ្មោះហាង (Sign Up)</button>
        </div>

        <form action="/login" method="POST" class="space-y-4" x-show="mode === 'login'">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Username</label>
                <input type="text" name="username" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="ឈ្មោះអ្នកប្រើប្រាស់">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Password</label>
                <input type="password" name="password" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 rounded-xl shadow-lg transition text-sm">Login to Store</button>
        </form>

        <form action="/signup" method="POST" class="space-y-4" x-show="mode === 'signup'" style="display: none;">
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Store Name (ឈ្មោះហាង)</label>
                <input type="text" name="store_name" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="ឧ. ហាងលក់ទំនិញ ABC">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Your Full Name (ឈ្មោះម្ចាស់ហាង)</label>
                <input type="text" name="admin_fullname" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="ឧ. សុខា">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Username (ឈ្មោះចូលប្រើ)</label>
                <input type="text" name="username" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="username">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Password (ពាក្យសម្ងាត់)</label>
                <input type="password" name="password" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500 transition" placeholder="••••••••">
            </div>
            <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 rounded-xl shadow-lg transition text-sm">Create Store & Account</button>
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
    <title>Store Dashboard - SaaS Inventory</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased">
    <div class="max-w-6xl mx-auto p-3 sm:p-6 lg:p-8" x-data="{ tab: 'dashboard' }">
        
        <!-- HEADER -->
        <header class="bg-gradient-to-r from-emerald-900 via-slate-900 to-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 shadow-xl">
            <div class="flex items-center space-x-3">
                <div class="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl shadow-inner">⚡</div>
                <div>
                    <h1 class="text-lg sm:text-xl font-bold text-white tracking-tight">Store Dashboard</h1>
                    <p class="text-xs text-emerald-400 font-medium mt-0.5">Store ID: {{ store_id }}</p>
                </div>
            </div>
            <div class="flex items-center justify-between w-full sm:w-auto space-x-3 border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-800">
                <span class="text-xs bg-slate-800/80 text-slate-300 border border-slate-700 px-3.5 py-2 rounded-xl flex items-center space-x-1.5 shadow-sm">
                    <span>👤</span> <span class="font-semibold">{{ current_user }}</span>
                </span>
                <a href="/logout" class="bg-red-500/10 hover:bg-red-500 text-red-400 hover:text-white border border-red-500/30 text-xs font-semibold px-4 py-2 rounded-xl transition shadow">Logout</a>
            </div>
        </header>

        <!-- NAVIGATION TABS -->
        <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 mb-6 bg-slate-900/80 backdrop-blur-md p-2 rounded-2xl border border-slate-800 shadow-lg">
            <button @click="tab = 'dashboard'" :class="tab === 'dashboard' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>🏠</span><span>Home</span></button>
            <button @click="tab = 'pos'" :class="tab === 'pos' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>🛒</span><span>POS Sell</span></button>
            <button @click="tab = 'add'" :class="tab === 'add' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>➕</span><span>Add Product</span></button>
            <button @click="tab = 'stock'" :class="tab === 'stock' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>📦</span><span>Stock</span></button>
            <button @click="tab = 'sales'" :class="tab === 'sales' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>📊</span><span>Sales History</span></button>
            <button @click="tab = 'logs'" :class="tab === 'logs' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800'" class="py-2.5 px-2 rounded-xl text-xs font-semibold text-center transition flex flex-col sm:flex-row items-center justify-center gap-1"><span>📋</span><span>Movement</span></button>
        </div>

        <!-- DASHBOARD HOME TAB (WITH CHARTS & LOW STOCK ALERTS) -->
        <div x-show="tab === 'dashboard'" class="space-y-6">
            <!-- STATS CARDS -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Items</p>
                    <p class="text-3xl font-bold text-white mt-2">{{ total_items }}</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Stock Qty</p>
                    <p class="text-3xl font-bold text-white mt-2">{{ total_stock }}</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Inventory Asset Value</p>
                    <p class="text-3xl font-bold text-emerald-400 mt-2">${{ "%.2f"|format(inventory_value) }}</p>
                </div>
            </div>

            <!-- CHARTS SECTION -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Sales Overview Chart -->
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <h3 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>📊</span> <span>ក្រាហ្វិកការលក់ (Sales Overview)</span></h3>
                    <div class="relative h-64">
                        <canvas id="salesChart"></canvas>
                    </div>
                </div>
                <!-- Stock Movement Distribution -->
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <h3 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>📈</span> <span>ចលនាស្តុក ចូល/ចេញ (Movement Summary)</span></h3>
                    <div class="relative h-64">
                        <canvas id="movementChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- LOW STOCK ALERT TABLE -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl overflow-x-auto">
                <h3 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2 text-amber-400"><span>⚠️</span> <span>ទំនិញជិតអស់ក្នុងស្តុក (Low Stock Alert < 10)</span></h3>
                <table class="w-full text-left border-collapse min-w-[500px]">
                    <thead>
                        <tr class="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                            <th class="p-3">Product Name</th>
                            <th class="p-3">Category</th>
                            <th class="p-3">Price</th>
                            <th class="p-3">Current Stock</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800 text-sm">
                        {% for p in low_stock_products %}
                        <tr class="hover:bg-slate-800/50 transition">
                            <td class="p-3 font-semibold text-white">{{ p.name }}</td>
                            <td class="p-3 text-slate-300">{{ p.category }}</td>
                            <td class="p-3 text-slate-300">${{ "%.2f"|format(p.price) }}</td>
                            <td class="p-3 font-bold text-amber-400">⚠️ {{ p.stock }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" class="p-6 text-center text-slate-500 italic">មិនមានទំនិញជិតអស់ក្នុងស្តុកទេ។ (ល្អណាស់!)</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- POS SELL TAB -->
        <div x-show="tab === 'pos'" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl max-w-xl mx-auto" style="display: none;">
            <h2 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>🛒</span> <span>POS - លក់ទំនិញ (Checkout)</span></h2>
            <form action="/sell" method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">ជ្រើសរើសទំនិញ (Select Product)</label>
                    <select name="product_id" required class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500">
                        <option value="">-- ជ្រើសរើសទំនិញ --</option>
                        {% for p in products %}
                        <option value="{{ p.id }}">{{ p.name }} (សល់ក្នុងស្តុក: {{ p.stock }} | តម្លៃ: ${{ "%.2f"|format(p.price) }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">ចំនួនលក់ (Quantity)</label>
                    <input type="number" name="quantity" min="1" value="1" required class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 rounded-xl shadow-lg transition text-sm">គិតលុយ និងកាត់ស្តុក (Confirm Sale)</button>
            </form>
        </div>

        <!-- ADD PRODUCT TAB -->
        <div x-show="tab === 'add'" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl max-w-xl mx-auto" style="display: none;">
            <h2 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>➕</span> <span>Add New Product</span></h2>
            <form action="/add" method="POST" class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Product Name</label>
                        <input type="text" name="name" required class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Price ($)</label>
                        <input type="number" step="0.01" name="price" required class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500">
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Category</label>
                        <input type="text" name="category" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500" value="General">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Initial Stock</label>
                        <input type="number" name="stock" required class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-emerald-500">
                    </div>
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 rounded-xl shadow-lg transition text-sm">Save Product</button>
            </form>
        </div>

        <!-- STOCK MANAGEMENT TAB -->
        <div x-show="tab === 'stock'" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl overflow-x-auto" style="display: none;">
            <h2 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>📦</span> <span>Stock Management</span></h2>
            <table class="w-full text-left border-collapse min-w-[500px]">
                <thead>
                    <tr class="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        <th class="p-3">Name</th>
                        <th class="p-3">Category</th>
                        <th class="p-3">Price</th>
                        <th class="p-3">Stock</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 text-sm">
                    {% for p in products %}
                    <tr class="hover:bg-slate-800/50 transition">
                        <td class="p-3 font-semibold text-white">{{ p.name }}</td>
                        <td class="p-3 text-slate-300">{{ p.category }}</td>
                        <td class="p-3 text-slate-300">${{ "%.2f"|format(p.price) }}</td>
                        <td class="p-3 font-bold text-emerald-400">{{ p.stock }}</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនមានទំនិញក្នុងស្តុកទេ។</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- SALES HISTORY TAB -->
        <div x-show="tab === 'sales'" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl overflow-x-auto" style="display: none;">
            <h2 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>📊</span> <span>Sales History (ប្រវត្តិការលក់)</span></h2>
            <table class="w-full text-left border-collapse min-w-[500px]">
                <thead>
                    <tr class="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        <th class="p-3">Product</th>
                        <th class="p-3">Qty</th>
                        <th class="p-3">Total ($)</th>
                        <th class="p-3">Date</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 text-sm">
                    {% for s in sales_list %}
                    <tr class="hover:bg-slate-800/50 transition">
                        <td class="p-3 font-semibold text-white">{{ s.product_name }}</td>
                        <td class="p-3 text-slate-300">{{ s.quantity }}</td>
                        <td class="p-3 text-emerald-400 font-bold">${{ "%.2f"|format(s.total_price) }}</td>
                        <td class="p-3 text-xs text-slate-500">{{ s.created_at }}</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនទាន់មានប្រវត្តិការលក់។</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- STOCK MOVEMENT TAB -->
        <div x-show="tab === 'logs'" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl overflow-x-auto" style="display: none;">
            <h2 class="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center space-x-2"><span>📋</span> <span>Stock Movement (ប្រវត្តិបម្រែបម្រួលស្តុក)</span></h2>
            <table class="w-full text-left border-collapse min-w-[500px]">
                <thead>
                    <tr class="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        <th class="p-3">Type</th>
                        <th class="p-3">Details</th>
                        <th class="p-3">Qty Change</th>
                        <th class="p-3">Date</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 text-sm">
                    {% for m in movements %}
                    <tr class="hover:bg-slate-800/50 transition">
                        <td class="p-3">
                            <span class="px-2.5 py-1 text-xs font-semibold rounded-lg {{ 'bg-red-500/10 text-red-400 border border-red-500/30' if m.type == 'OUT' else 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' }}">{{ m.type }}</span>
                        </td>
                        <td class="p-3 text-slate-300">{{ m.description }}</td>
                        <td class="p-3 font-bold {{ 'text-red-400' if m.type == 'OUT' else 'text-emerald-400' }}">{{ m.qty_change }}</td>
                        <td class="p-3 text-xs text-slate-500">{{ m.created_at }}</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="4" class="p-8 text-center text-slate-500 italic">មិនទាន់មានទិន្នន័យ Stock Movement.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

    </div>

    <!-- SCRIPT FOR CHARTS -->
    <script>
        const salesData = {{ sales_chart_data | safe }};
        const movementData = {{ movement_chart_data | safe }};

        // Sales Chart
        new Chart(document.getElementById('salesChart'), {
            type: 'line',
            data: {
                labels: salesData.labels,
                datasets: [{
                    label: 'Total Sales ($)',
                    data: salesData.values,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } },
                    y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } }
                }
            }
        });

        // Movement Chart
        new Chart(document.getElementById('movementChart'), {
            type: 'bar',
            data: {
                labels: ['IN (ទិញចូល)', 'OUT (លក់ចេញ)'],
                datasets: [{
                    data: [movementData.in, movementData.out],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } }
                }
            }
        });
    </script>
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
    
    # Low stock products (e.g. stock < 10)
    low_stock_products = [p for p in products if int(p.get("stock", 0) or 0) < 10]

    # Prepare Chart Data
    sales_labels = [s.get("created_at", "")[:10] for s in sales_list[-7:]]
    sales_values = [float(s.get("total_price", 0) or 0) for s in sales_list[-7:]]
    sales_chart_data = {"labels": sales_labels if sales_labels else ["គ្មានទិន្នន័យ"], "values": sales_values if sales_values else [0]}

    in_count = sum(1 for m in movements if m.get("type") == "IN")
    out_count = sum(1 for m in movements if m.get("type") == "OUT")
    movement_chart_data = {"in": in_count, "out": out_count}
    
    return render_template_string(INDEX_TEMPLATE, 
                           products=products, 
                           sales_list=sales_list,
                           movements=movements,
                           low_stock_products=low_stock_products,
                           total_items=total_items, 
                           total_stock=total_stock, 
                           inventory_value=inventory_value,
                           sales_chart_data=json.dumps(sales_chart_data),
                           movement_chart_data=json.dumps(movement_chart_data),
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

