from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time

app = FastAPI()

def db_status():
    while True:
        try:
            db_connect = mysql.connector.connect(
                # host=os.getenv('DB_CN_CINEMA'),
                # user=os.getenv('DB_USERNAME'),
                # password=os.getenv('DB_PASSWORD'),
                # database=os.getenv('DB_DATABASE')
                host="localhost",
                port="33061",
                user="user",
                password="password",
                database="cinema_db"
            )
            return db_connect
        except:
            print("Подключение к БД...")
            time.sleep(2)



@app.get("/session/{session_id}")
def get_session(session_id: int):
    conn = db_status()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT
        m.title AS movie_title,
        m.release_year,
        m.image_path,
        s.session_date,
        h.description AS hall_name,
        s.seats_map
    FROM sessions s
    JOIN movies m ON s.movie_id = m.id
    JOIN halls h ON s.hall_id = h.id
    WHERE s.id = %s    
    """
    try:
        cursor.execute(query, (session_id,))
        info_session = cursor.fetchone() #одна строка 
        if not info_session:
            return{"error": "Сеанс не найден"}
        return info_session
    finally:
        cursor.close()
        conn.close()

@app.get("/film_info/list")
def get_film_list():
    conn = db_status()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT *
    FROM movies
    LIMIT 10
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall() #Все строки
        if not result:
            return{"error": "Сеанс не найден"}
        return result
    finally:
        cursor.close()
        conn.close()


@app.get("/film_info/{film_id}")
def get_film_info(film_id: int):
    conn = db_status()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT
       s.session_date,
       h.id,
       h.description AS hall_name
    FROM sessions s
    JOIN movies m ON s.movie_id = m.id
    JOIN halls h ON s.hall_id = h.id
    WHERE s.id = %s
    """
    try:
        cursor.execute(query, (film_id,))
        result = cursor.fetchall() #Все строки
        if not result:
            return{"error": "Информация о фильме не найдена"}
        return result
    finally:
        cursor.close()
        conn.close()

