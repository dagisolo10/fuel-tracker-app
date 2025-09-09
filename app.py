from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
today = date.today()

# Database setup
conn = sqlite3.connect('Truck.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuel_record (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Truck TEXT NOT NULL,
        Fuel REAL NOT NULL,
        Cost REAL NOT NULL,
        Date TEXT NOT NULL
    )
""")
conn.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    trucks = ['AA A-65987', 'AA B-42259']
    today = date.today()

    if request.method == 'POST':
        truck = request.form['truck']
        fuel = float(request.form['fuel'])
        cost = float(request.form['cost'])


        

        cursor.execute("""
            INSERT INTO fuel_record (Truck, Fuel, Cost, Date)
            VALUES (?, ?, ?, ?)
        """, (truck, fuel, cost, today))
        conn.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM fuel_record ORDER BY Date DESC")
    records = cursor.fetchall()
    return render_template('index.html', refills=records, trucks=trucks)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor.execute("DELETE FROM fuel_record WHERE id = ?", (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
