from flask import Flask, render_template, request, jsonify
from tax_calculator import calculate_tax_distribution
import os
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/states')
def get_states():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT state FROM tax_rates ORDER BY state')
        states = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(states)
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/api/calculate_tax', methods=['POST'])
def calculate_tax():
    try:
        data = request.json
        monthly_salary = float(data['salary'])
        state = data['state']

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch tax rates for the selected state
        cur.execute('SELECT * FROM tax_rates WHERE state = %s', (state,))
        tax_rates = cur.fetchone()
        
        cur.close()
        conn.close()

        if not tax_rates:
            return jsonify({'error': 'Invalid state selected'}), 400

        # Calculate tax distribution
        tax_distribution = calculate_tax_distribution(monthly_salary, tax_rates)
        
        return jsonify(tax_distribution)
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
