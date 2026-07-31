<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Lux Store - Professional Inventory SaaS</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    
    <div class="max-w-5xl mx-auto p-4 sm:p-6" x-data="{ tab: 'dashboard' }">
        
        <!-- Header Banner -->
        <header class="bg-slate-800 border border-slate-700 rounded-xl p-4 sm:p-5 flex flex-col sm:flex-row justify-between items-center mb-6 shadow-lg">
            <div class="flex items-center space-x-3 mb-3 sm:mb-0">
                <span class="text-2xl">⚡</span>
                <div>
                    <h1 class="text-lg sm:text-xl font-bold tracking-wide">Modern Lux Store</h1>
                    <p class="text-xs text-slate-400">Professional Inventory SaaS for SMEs</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <span class="inline-block w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></span>
                <span class="text-xs text-slate-300">Supabase Connected</span>
            </div>
        </header>

        <!-- Navigation Tabs Switcher (4 Standard Sections) -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-6 border-b border-slate-800 pb-4">
            <button @click="tab = 'dashboard'" :class="tab === 'dashboard' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition flex items-center justify-center space-x-2">
                <span>📊</span> <span>1. Dashboard</span>
            </button>
            <button @click="tab = 'list'" :class="tab === 'list' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition flex items-center justify-center space-x-2">
                <span>📦</span> <span>2. Inventory List</span>
            </button>
            <button @click="tab = 'add'" :class="tab === 'add' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition flex items-center justify-center space-x-2">
                <span>➕</span> <span>3. Add / Stock In</span>
            </button>
            <button @click="tab = 'reports'" :class="tab === 'reports' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition flex items-center justify-center space-x-2">
                <span>📈</span> <span>4. Reports & Value</span>
            </button>
        </div>

        <!-- TAB 1: DASHBOARD & ANALYTICS -->
        <div x-show="tab === 'dashboard'" class="space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-slate-800 border border-slate-700 p-4 rounded-xl shadow">
                    <p class="text-xs text-slate-400 font-medium uppercase">Total Items</p>
                    <p class="text-3xl font-bold mt-1 text-white">{{ total_items }}</p>
                    <p class="text-xs text-blue-400 mt-2">មុខទំនិញសរុបក្នុងស្តុក</p>
                </div>
                <div class="bg-slate-800 border border-slate-700 p-4 rounded-xl shadow">
                    <p class="text-xs text-slate-400 font-medium uppercase">Total Stock Qty</p>
                    <p class="text-3xl font-bold mt-1 text-white">{{ total_stock }}</p>
                    <p class="text-xs text-amber-400 mt-2">បរិមាណទំនិញសរុប</p>
                </div>
                <div class="bg-slate-800 border border-slate-700 p-4 rounded-xl shadow">
                    <p class="text-xs text-slate-400 font-medium uppercase">Inventory Value</p>
                    <p class="text-3xl font-bold mt-1 text-emerald-400">${{ "%.2f"|format(inventory_value) }}</p>
                    <p class="text-xs text-emerald-500 mt-2">ទឹកប្រាក់សរុបក្នុងស្តុក</p>
                </div>
            </div>

            <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg">
                <h2 class="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">សេចក្តីសង្ខេបប្រព័ន្ធ (System Overview)</h2>
                <p class="text-sm text-slate-400 leading-relaxed">
                    ស្វាគមន៍មកកាន់ប្រព័ន្ធគ្រប់គ្រងស្តុកទំនិញសម្រាប់អាជីវកម្ម SMEs នៅកម្ពុជា។ បងអាចប្រើប្រាស់ Tab ខាងលើដើម្បីមើលបញ្ជីស្តុក បញ្ចូលទំនិញថ្មី និងពិនិត្យរបាយការណ៍តម្លៃសរុបបានយ៉ាងងាយស្រួល។
                </p>
            </div>
        </div>

        <!-- TAB 2: INVENTORY LIST TABLE -->
        <div x-show="tab === 'list'" class="bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-lg" style="display: none;">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-sm font-semibold text-slate-300 uppercase tracking-wider">បញ្ជីស្តុកទំនិញបច្ចុប្បន្ន</h2>
                <span class="text-xs bg-slate-700 px-2.5 py-1 rounded-md text-slate-300">Total: {{ total_items }} items</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-slate-700 text-xs text-slate-400 uppercase">
                            <th class="p-3">Name</th>
                            <th class="p-3">Category</th>
                            <th class="p-3">Price ($)</th>
                            <th class="p-3">Stock Qty</th>
                            <th class="p-3 text-right">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-700/50 text-sm">
                        {% for p in products %}
                        <tr class="hover:bg-slate-700/30 transition">
                            <td class="p-3 font-medium text-white">{{ p.name }}</td>
                            <td class="p-3 text-slate-300">{{ p.category }}</td>
                            <td class="p-3 text-emerald-400">${{ "%.2f"|format(p.price) }}</td>
                            <td class="p-3">
                                <span :class="{{ p.stock }} <= 5 ? 'text-amber-400 font-bold' : 'text-slate-100'">
                                    {{ p.stock }}
                                </span>
                            </td>
                            <td class="p-3 text-right">
                                {% if p.stock <= 5 %}
                                <span class="text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full">Low Stock</span>
                                {% else %}
                                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full">In Stock</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" class="p-6 text-center text-slate-500 italic">មិនទាន់មានទំនិញនៅក្នុងស្តុកឡើយ។ សូមចូលទៅកាន់ Tab "Add / Stock In" ដើម្បីបញ្ចូលថ្មី។</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: ADD NEW PRODUCT & STOCK IN -->
        <div x-show="tab === 'add'" class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg" style="display: none;">
            <h2 class="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">បញ្ចូលទំនិញថ្មី / បន្ថែមស្តុក (Stock In)</h2>
            <form action="/add" method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-medium text-slate-400 mb-1">Product Name</label>
                    <input type="text" name="name" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 text-sm" placeholder="បញ្ចូលឈ្មោះទំនិញ...">
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Category</label>
                        <select name="category" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 text-sm">
                            <option value="Watches">Watches</option>
                            <option value="Electronics">Electronics</option>
                            <option value="Accessories">Accessories</option>
                            <option value="Clothing">Clothing</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Stock Qty</label>
                        <input type="number" name="stock" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 text-sm" placeholder="0">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-400 mb-1">Price ($)</label>
                    <input type="number" step="0.01" name="price" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 text-sm" placeholder="0.00">
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2.5 rounded-lg shadow transition text-sm mt-2">
                    Save Product to Supabase
                </button>
            </form>
        </div>

        <!-- TAB 4: REPORTS & ANALYTICS -->
        <div x-show="tab === 'reports'" class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg space-y-4" style="display: none;">
            <h2 class="text-sm font-semibold text-slate-300 uppercase tracking-wider">របាយការណ៍វាយតម្លៃស្តុក (Inventory Valuation Reports)</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div class="bg-slate-900 border border-slate-700/60 p-4 rounded-xl">
                    <p class="text-xs text-slate-400">Total Capital / Asset Value</p>
                    <p class="text-xl font-bold text-emerald-400 mt-1">${{ "%.2f"|format(inventory_value) }}</p>
                    <p class="text-[11px] text-slate-500 mt-1">តម្លៃសរុបនៃទំនិញដែលមានស្រាប់ក្នុងស្តុកបច្ចុប្បន្ន</p>
                </div>
                <div class="bg-slate-900 border border-slate-700/60 p-4 rounded-xl">
                    <p class="text-xs text-slate-400">Total Products Variety</p>
                    <p class="text-xl font-bold text-blue-400 mt-1">{{ total_items }} Types</p>
                    <p class="text-[11px] text-slate-500 mt-1">ចំនួនប្រភេទមុខទំនិញសរុប</p>
                </div>
            </div>
        </div>

    </div>

</body>
</html>
