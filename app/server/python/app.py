from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import time
import json
from typing import List

app = FastAPI()

class ReserveRequest(BaseModel):
    seats_map: List[List[int]]

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

@app.post("/session/{session_id}/reserve")
def reserve_seats(session_id: int, req: ReserveRequest):
    conn = db_status()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Получаем АКТУАЛЬНОЕ состояние из базы
        cursor.execute("SELECT seats_map FROM sessions WHERE id = %s", (session_id,))
        db_data = cursor.fetchone()
        
        if not db_data:
            return {"status": "error", "message": "Сеанс не найден"}
            
        current_map = json.loads(db_data['seats_map']) # То, что в базе сейчас
        user_map = req.seats_map # То, что прислал пользователь
        
        warnings = []
        changes_made = False

        # 2. Двойной цикл для сверки
        # Проходим по рядам
        for r in range(len(current_map)):
            # Проходим по местам в ряду
            for c in range(len(current_map[r])):
                
                # Если пользователь хочет забронировать (прислал 2)
                if user_map[r][c] == 2:
                    
                    # ПРОВЕРКА: Если в базе это место уже КУПЛЕНО (1) или уже ЗАБРОНИРОВАНО кем-то другим (2)
                    if current_map[r][c] != 0:
                        warnings.append(f"Ряд {r+1}, место {c+1} уже занято или забронировано.")
                    else:
                        # Если место было свободным (0), обновляем его в нашей локальной копии
                        current_map[r][c] = 2
                        changes_made = True

        # 3. Анализируем результат
        if warnings:
            # Если есть хоть одна ошибка, мы НЕ сохраняем ничего и возвращаем список ошибок
            return {
                "status": "warning",
                "message": "Некоторые места не удалось забронировать",
                "errors": warnings,
                "actual_map": current_map # Возвращаем актуальную карту, чтобы клиент обновился
            }
        
        if changes_made:
            # Если всё чисто, сохраняем обновленную карту в базу
            new_map_json = json.dumps(current_map)
            cursor.execute("UPDATE sessions SET seats_map = %s WHERE id = %s", 
                           (new_map_json, session_id))
            conn.commit()
            return {"status": "ok", "message": "Места успешно забронированы"}
        
        return {"status": "error", "message": "Вы не выбрали ни одного места"}

    finally:
        cursor.close()
        conn.close()

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