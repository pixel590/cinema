import requests

SERVER_URL = "http://localhost:5000"

def get_status():
    try:
        response = requests.get(f"{SERVER_URL}/value")
        return response.json().get('value')
    except:
        return "Ошибка связи"

def change_status():
    new_val = input("Введите новый статус: ")
    try:
        #Изменение данных
        response = requests.put(
            f"{SERVER_URL}/value", 
            json={"value": new_val}
        )
        if response.status_code == 200:
            print("Успешно обновлено!")
        else:
            print(f"Ошибка: {response.json().get('detail')}")
    except:
        print("Сервер недоступен")

while True:
    type = int(input("Меню\n\t1-информация\n\t2-Обновить запись\nВвод: "))
    match type:
        case 1:
            print("Результат: ",end="")
            print(get_status())
        case 2:
            change_status()