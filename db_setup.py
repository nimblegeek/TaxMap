import os
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

def create_tax_rates_table():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tax_rates (
        id SERIAL PRIMARY KEY,
        state VARCHAR(50) UNIQUE NOT NULL,
        federal_rate DECIMAL(5,2) NOT NULL,
        state_rate DECIMAL(5,2) NOT NULL,
        local_rate DECIMAL(5,2) NOT NULL,
        social_security_rate DECIMAL(5,2) NOT NULL,
        medicare_rate DECIMAL(5,2) NOT NULL
    )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def insert_sample_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    sample_data = [
        ('California', 22.0, 9.3, 1.0, 6.2, 1.45),
        ('New York', 22.0, 6.85, 3.88, 6.2, 1.45),
        ('Texas', 22.0, 0.0, 1.0, 6.2, 1.45),
        ('Florida', 22.0, 0.0, 1.0, 6.2, 1.45),
        ('Illinois', 22.0, 4.95, 1.0, 6.2, 1.45)
    ]
    
    cur.executemany('''
    INSERT INTO tax_rates (state, federal_rate, state_rate, local_rate, social_security_rate, medicare_rate)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (state) DO UPDATE SET
    federal_rate = EXCLUDED.federal_rate,
    state_rate = EXCLUDED.state_rate,
    local_rate = EXCLUDED.local_rate,
    social_security_rate = EXCLUDED.social_security_rate,
    medicare_rate = EXCLUDED.medicare_rate
    ''', sample_data)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_tax_rates_table()
    insert_sample_data()
    print("Database setup completed successfully.")
