from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import json

app = Flask(__name__)

SUPABASE_URL = "https://dwqyrlrylworstasglsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3cXlybHJ5bHdvcnN0YXNnbHNpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTUwNTc3MCwiZXhwIjoyMTAxMDgxNzcwfQ.gR5rqaHs44_4pH-ufkdRRhsx1rt2jEAnP1d905Go5Rc"

@app.route('/')
def index():
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/products?select=*",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
        )
        with urllib.request.urlopen(req) as response:
            products = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching: {e}")
        products = []
    
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    
    if name and quantity and price:
        try:
            data = json.dumps({
                "name": name,
                "quantity": int(quantity),
                "price": float(price)
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/products",
                data=data,
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                },
                method="POST"
            )
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Error inserting: {e}")
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

