import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
DB_LOCATION=os.getenv("DB_LOCATION")


connection = sqlite3.connect(str(DB_LOCATION))
cursor = connection.cursor()

# Create a user_login_data in SQLite
cursor.execute(
'''
CREATE TABLE user_login_data (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE,
    salt TEXT,
    password_hash TEXT,
    email VARCHAR(50) UNIQUE,
    otp_generated INTEGER,
    otp_generation_time INTEGER,
    verification_status INTEGER
)
'''
)

connection.commit()
connection.close()