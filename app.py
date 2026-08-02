import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bizstockkh_super_secret_key_2026")

# Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==================== HTML / FRONTEND TEMPLATE ====================
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizStockKH</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased" 
      x-data="{ 
          tab: 'dashboard', 
          lang: 'km',
          t: {
              km: {
                  title: 'BizStockKH',
                  storeId: 'លេខសម្គាល់ហាង: 1',
                  logout: 'ចាកចេញ',
                  home: 'ទំព័រដើម',
                  pos: 'កន្រ្តកលក់ (POS)',
                  addProduct: 'បន្ថែមទំនិញ',
                  expenses: 'ចំណាយ',
                  stock: 'ស្តុកទំនិញ',
                  salesHistory: 'ប្រវត្តិលក់',
                  movement: 'ចលនាទំនិញ',
                  totalSales: 'ទឹកប្រាក់លក់សរុប',
                  totalExpenses: 'ចំណាយសរុប',
                  netProfit: 'ចំណេញសុទ្ធ'
              },
              en: {
                  title: 'BizStockKH',
                  storeId: 'Store ID: 1',
                  logout: 'Logout',
                  home: 'Home',
                  pos: 'POS Cart',
                  addProduct: 'Add Product',
                  expenses: 'Expenses',
                  stock: 'Stock',
                  salesHistory: 'Sales History',
                  movement: 'Movement',
                  totalSales: 'TOTAL SALES',
                  totalExpenses: 'TOTAL EXPENSES',
                  netProfit: 'NET PROFIT'
              }
          }
      }">

<div class="max-w-7xl mx-auto p-3 sm:p-6 lg:p-8">

    <!-- HEADER -->
    <header class="bg-gradient-to-r from-emerald-900 via-slate-900 to-slate-900 p-4 sm:p-6 rounded-2xl shadow-xl border border-emerald-500/20 mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-2xl shadow-inner">
                ⚡
            </div>
            <div>
                <h1 class="text-lg sm:text-xl font-bold text-white tracking-wide" x-text="t[lang].title">BizStockKH</h1>
                <p class="text-xs text-emerald-400 font-medium mt-0.5" x-text="t[lang].storeId">Store ID: 1</p>
            </div>
        </div>

        <!-- LANGUAGE SWITCHER & USER INFO -->
        <div class="flex items-center space-x-3">
            <!-- Language Toggle Button -->
            <button @click="lang = lang === 'km' ? 'en' : 'km'" class="px-3 py-1.5 rounded-lg bg-slate-800 text-xs font-semibold border border-slate-700 hover:bg-slate-700 transition">
                🌐 <span x-text="lang === 'km' ? 'English' : 'ភាសាខ្មែរ'"></span>
            </button>

            <div class="flex items-center space-x-2 bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-800 text-xs">
                <span>👤</span>
                <span class="font-semibold text-slate-300">{{ current_user }}</span>
            </div>
            <a href="/logout" class="bg-red-500/10 hover:bg-red-500/20 text-red-400 px-3 py-1.5 rounded-xl text-xs font-semibold border border-red-500/20 transition" x-text="t[lang].logout">ចាកចេញ</a>
        </div>
    </header>

    <!-- NAVIGATION TABS -->
    <div class="grid grid-cols-3 sm:grid-cols-7 gap-2 mb-6 bg-slate-900/50 p-2 rounded-2xl border border-slate-800/80">
        <button @click="tab = 'dashboard'" :class="tab === 'dashboard' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">🏠</span>
            <span x-text="t[lang].home">ទំព័រដើម</span>
        </button>
        <button @click="tab = 'pos'" :class="tab === 'pos' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">🛒</span>
            <span x-text="t[lang].pos">POS Cart</span>
        </button>
        <button @click="tab = 'add_product'" :class="tab === 'add_product' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">➕</span>
            <span x-text="t[lang].addProduct">បន្ថែមទំនិញ</span>
        </button>
        <button @click="tab = 'expenses'" :class="tab === 'expenses' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">💸</span>
            <span x-text="t[lang].expenses">ចំណាយ</span>
        </button>
        <button @click="tab = 'stock'" :class="tab === 'stock' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">📦</span>
            <span x-text="t[lang].stock">ស្តុកទំនិញ</span>
        </button>
        <button @click="tab = 'history'" :class="tab === 'history' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">📊</span>
            <span x-text="t[lang].salesHistory">ប្រវត្តិលក់</span>
        </button>
        <button @click="tab = 'movement'" :class="tab === 'movement' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40' : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'" class="flex flex-col items-center justify-center py-2.5 px-2 rounded-xl text-xs font-medium transition">
            <span class="text-base mb-1">📋</span>
            <span x-text="t[lang].movement">ចលនាទំនិញ</span>
        </button>
    </div>

    <!-- TAB CONTENT: DASHBOARD -->
    <div x-show="tab === 'dashboard'" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider" x-text="t[lang].totalSales">TOTAL SALES</p>
                <p class="text-2xl font-bold text-emerald-400 mt-2">${{ "%.2f"|format(total_sales) }}</p>
            </div>
            <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider" x-text="t[lang].totalExpenses">TOTAL EXPENSES</p>
                <p class="text-2xl font-bold text-rose-400 mt-2">${{ "%.2f"|format(total_expenses) }}</p>
            </div>
            <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider" x-text="t[lang].netProfit">NET PROFIT</p>
                <p class="text-2xl font-bold text-cyan-400 mt-2">${{ "%.2f"|format(net_profit) }}</p>
            </div>
        </div>
    </div>

    <!-- OTHER TABS PLACEHOLDER (สามารถเพิ่มเนื้อหาหน้าอื่น ๆ ต่อตรงนี้ได้) -->
    <div x-show="tab !== 'dashboard'" class="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-center text-slate-400">
        <p class="text-lg">មុខងារនេះកំពុងដំណើរការ... (Content for <span x-text="tab"></span>)</p>
    </div>

</div>

</body>
</html>
"""

AUTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizStockKH - Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-2xl">
        <div class="text-center mb-6">
            <div class="text-4xl mb-2">📦</div>
            <h1 class="text-xl font-bold text-white">BizStockKH</h1>
            <p class="text-xs text-slate-400 mt-1">សូមចូលប្រើប្រាស់ប្រព័ន្ធរបស់អ្នក</p>
        </div>
        {% if error %}
        <div class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3 rounded-xl text-xs mb-4 text-center">
            {{ error }}
        </div>
        {% endif %}
        <form method="POST" class="space-y-4">
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">ឈ្មោះអ្នកប្រើប្រាស់ (Username)</label>
                <input type="text" name="username" required class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">ពាក្យសម្ងាត់ (Password)</label>
                <input type="password" name="password" required class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
            </div>
            <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 rounded-xl text-sm transition shadow-lg shadow-emerald-900/30">
                ចូលប្រព័ន្ធ (Login)
            </button>
        </form>
    </div>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # គំរូផ្ទៀងផ្ទាត់សាមញ្ញ (អាចកែសម្រួលជាមួយ Supabase Auth តាមចង់បាន)
        if username == "admin" and password == "123456":
            session["user"] = username
            return redirect(url_for("index"))
        else:
            error = "ឈ្មោះអ្នកប្រើប្រាស់ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"
    return render_template_string(AUTH_TEMPLATE, error=error)

@app.route("/dashboard")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    
    # តម្លៃគំរូសម្រាប់ផ្ទៀងផ្ទាត់ Dashboard (អាចទាញពី Supabase តាមកូដเดิมរបស់បង)
    total_sales = 57.00
    total_expenses = 0.00
    net_profit = total_sales - total_expenses

    return render_template_string(
        INDEX_TEMPLATE, 
        current_user=session["user"],
        total_sales=total_sales,
        total_expenses=total_expenses,
        net_profit=net_profit
    )

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

