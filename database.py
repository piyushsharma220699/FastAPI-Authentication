import sqlite3

connection = sqlite3.connect('./sqlite.db')
cursor = connection.cursor()

# Create a user_login_data in SQLite
cursor.execute(
'''
CREATE TABLE user_login_data (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE,
    salt TEXT,
    password_hash TEXT
)
'''
)

connection.commit()
connection.close()