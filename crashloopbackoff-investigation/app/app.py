import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "payments")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connected to PostgreSQL")
except Exception as e:
    print(f"panic: {e}")
    exit(1)

@app.route("/")
def home():
    return "Payment Service Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
