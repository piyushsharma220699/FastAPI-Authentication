from fastapi import FastAPI, Body, HTTPException
import hashlib
from dotenv import load_dotenv
import os
import sqlite3
import secrets

load_dotenv()

DB_LOCATION=os.getenv("DB_LOCATION")

app = FastAPI()

@app.post("/api/v1/register")
def register_user(username: str = Body(), password: str = Body()):
    salt = str(secrets.token_bytes(16).hex())
    password_with_salt = password + salt

    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()

    try:
        connection = sqlite3.connect(database=str(DB_LOCATION))
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO user_login_data (username, salt, password_hash)
            VALUES (?,?,?)
        ''', (username,salt,hashed_password))
        
        connection.commit()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=400 ,detail=str(e))

    return {"user_id" : username}

@app.get('/api/v1/login')
def login_user(username: str, password: str):
    try:
        connection = sqlite3.connect(database=str(DB_LOCATION))
        cursor = connection.cursor()

        cursor.execute('''
            SELECT * FROM user_login_data
            WHERE username=?
        ''',username)
        
        connection.commit()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=400 ,detail=str(e))
    
    return {"data" : "Welcome to TerraVision!"}