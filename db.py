import sqlite3
from datetime import datetime

DB_NAME = "health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    hba1c REAL,
    systolic REAL,
    diastolic REAL,
    temperature REAL,
    spo2 REAL,
    heart_rate REAL,
    score INTEGER
)
    """)

    conn.commit()
    conn.close()

def insert_record(data, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
INSERT INTO records (timestamp, weight, height, bmi, hba1c, systolic, diastolic, temperature, spo2, heart_rate, score)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    data["weight"],
    data["height"],
    data["bmi"],
    data["hba1c"],
    data["systolic"],
    data["diastolic"],
    data["temperature"],
    data["spo2"],
    data["heart_rate"],
    score
))

    conn.commit()
    conn.close()

import pandas as pd

def fetch_records():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM records ORDER BY timestamp", conn)
    conn.close()
    return df