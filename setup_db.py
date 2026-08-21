import sqlite3

conn = sqlite3.connect("hotel.db")

with open('schema.sql', 'r') as f:
    sql = f.read()

conn.executescript(sql)
conn.commit()
conn.close()

print("Database setup complete! Run 'python main.py' to start.")