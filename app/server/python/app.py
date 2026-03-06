from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time
import json
import os
from typing import List

app = FastAPI()

class ReserveRequest(BaseModel):
    seats_map: List[List[int]]

def db_status():
    while True:
        try:
            db_connect = mysql.connector.connect(
                host=os.getenv('DB_CN_CINEMA'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE'),
                port="3306"
            )
            return db_connect
        except:
            print("Подключение к БД...")
            time.sleep(2)


@app.post("/session/{session_id}/reserve")

@app.get("/session/{session_id}")



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)