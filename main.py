from fastapi import FastAPI, Body, HTTPException
import hashlib
from dotenv import load_dotenv
from email.message import EmailMessage
import os
import random
import secrets
import smtplib
import sqlite3
import time

load_dotenv()

DB_LOCATION=os.getenv("DB_LOCATION")
VERIFICATION_EMAIL_ID=os.getenv("VERIFICATION_EMAIL_ID")
VERIFICATION_PASSWORD=os.getenv("VERIFICATION_PASSWORD")

app = FastAPI()

def send_otp_to_user(email: str, otp: int):
    message = EmailMessage()
    message.set_content(f"Your OTP Code is: {otp}")
    message["Subject"] = "TerraVision OTP Verification"
    message["From"] = VERIFICATION_EMAIL_ID
    message["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(str(VERIFICATION_EMAIL_ID),str(VERIFICATION_PASSWORD))
        server.send_message(message)
        
@app.post("/api/v1/register")
def register_user(username: str = Body(), password: str = Body(), email: str = Body()):
    salt = str(secrets.token_bytes(16).hex())
    password_with_salt = password + salt

    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()

    otp_generated = random.randint(100000,999999)
    otp_generation_time = int(time.time())

    try:
        connection = sqlite3.connect(database=str(DB_LOCATION))
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO user_login_data (username, salt, password_hash, email, otp_generated, otp_generation_time, verification_status)
            VALUES (?,?,?,?,?,?,?)
        ''', (username,salt,hashed_password,email,otp_generated,otp_generation_time,1))
        
        connection.commit()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=400 ,detail=str(e))

    send_otp_to_user(email,otp_generated)

    return {"user_id" : username, "message" : "User Successfully Registered. You have received a mail on the above E-Mail ID. Please verify your identity to move forward."}

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