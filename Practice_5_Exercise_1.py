import os
import sys
import keyboard
import json

list_main = []
list_width = 16
list_height = 12
tab = 4
tab_mass = 4

price_list=[]

# заполнение списка цен
for i in range(list_height):
    cut_price = 3
    if(i < list_height//cut_price): price_list.append(500)
    elif(i < (list_height//cut_price)*2): price_list.append(300)
    else: price_list.append(100)

#общая ширина + заголовок
total_width = (tab+1) + (list_width*tab_mass)
save_file = "cinema_data.json" # Имя файла для хранения

def save_data():
    with open(save_file, 'w', encoding='utf-8') as f:
        json.dump(list_main, f)

def load_data():
    if os.path.exists(save_file):
        with open(save_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

#Подзадача 1
#Подзадача 9
def mass_init():
    global list_main
    saved_data = load_data()
    if saved_data:
        list_main = saved_data
        print("--- Данные загружены из файла ---")
    else:
        for i in range(list_height):
            temp = [0] * list_width
            list_main.append(temp)
        print("--- Создан новый зал ---")

#Подзадача 5
#Печать текста
def display_cinema_print():
    print(f"{"Места":^{total_width }}", "\n") 

    #Подзадача 2
    print(f"{"":<{tab+1}}", end="") # отступ угол
    #+1 для ровности

    #Номер места (+1)
    for i in range(list_width):
        print(f"{i+1:<{tab_mass}}", end="")
    print("\nРяд")

    #список вывод
    for i in range(list_height):
        print(f"{i+1:<{tab}}", end="") #номер ряда (c нуля +1) + отступ
        for j in range(list_width):
            print(f"{list_main[i][j]:^{tab_mass}}", end="")
        if(i < list_height): print(f"{price_list[i]} руб.")

#Вспомогательные функции
#Очистка всего
def display_clear():
    os.system('cls')

def display_reload():
    display_clear()
    display_cinema_print()

def display_legend():
    display_cinema_print()
    print("\n0 - место свободно")
    print("1 - место забронировано Вами")
    print("2 - место занято")

#режимы функции
display_cinema_print.clear = display_clear
display_cinema_print.reload = display_reload
display_cinema_print.legend = display_legend

# Подзадача 12
def display_price():
    total_price = 0
    for j in range(list_height):
        for i in range(list_width):
            if(list_main[j][i] == 2):
                total_price += price_list[j]
    print(f"\tИтоговая цена {total_price} рублей.")

def only_int(x):
    try:
       return int(x)
    except ValueError:
        while not isinstance(x, int):
           print("Ошибка, введите число!")
           #Какое-то масло масленное
           try:
                x = int(input("Ввод: "))
           except ValueError:
               print("ТОЛЬКО ЧИСЛА!")
    return x

#Подзадача 4
#место, ряд
def get_edit_place():
    row = 0
    place = 0
    #ряд
    while not (0 < row <= list_height):
        row = only_int(input("Введите интересующий ряд: "))
        if not (0 < row <= list_height):
            print(f"Диапазон от 1 до {list_height}")
    #Место
    while not (0 < place <= list_width):
        place =  only_int(input("Введите интересующее место: "))
        if not (0 < place <= list_width):
            print(f"Диапазон от 1 до {list_width}")

    print(f"Вы выбрали {place} место на {row} ряду")
    row=row-1
    place=place-1
    return place,row

#Подзадача 11.2
def edit_place_v2():
    x_start,y_start = get_edit_place() #место, ряд
    position = y_start * list_width + x_start
    all_position = list_width * list_height

    #число свободных мест
    free_plaice = 0
    for j in range(list_height):
        for i in range(list_width):
            if(list_main[j][i] == 0): free_plaice += 1
    print(f"В зале всего {all_position} мест! Из них свободно {free_plaice}")

    selected = only_int(input("Введите количество мест которые хотите купить: "))

    while selected > free_plaice:
        print(f"Ошибка, в зале всего {all_position} мест! Из них свободно {free_plaice}!!")
        selected = only_int(input("Введите корректное число: "))
    checked = 0 #счетчик
    processed = 0#счетчик
    skip = 0

    while (processed < selected) and (checked < all_position):
        position_now = (position+checked)%all_position 
        x = position_now % list_width
        y = position_now // list_width
        if(list_main[y][x] == 1):
            print(f"----\nМесто {x+1} на {y+1} ряду занято")
            skip += 1
        elif(list_main[y][x] == 0):
            list_main[y][x] = 2
            print(f"----\nМесто {x+1} на {y+1} ряду выделено")
            processed += 1
        else:
            print("Что-то пошло не так")
        checked += 1
    
    display_cinema_print()
    print(f"\nРезультат:\n\tВыделено {processed} ячеек.\n\tПропущено {skip} ячеек.")

# Подзадача 8
def buy_place():
    # Подзадача 9 проверка, есть ли вообще выбранные места
    check_mass_for_2_value = 0
    for j in range(list_height):
                for i in range(list_width):
                    if list_main[j][i] == 2: check_mass_for_2_value += 1
    
    if(check_mass_for_2_value > 0):
        display_price()
        choose = only_int(input("Вы действительно хотите купить билеты?\n\t1-Да\n\t2-Нет (очистить всe)\nВведите: "))
        match choose:
            case 1:
                for j in range(list_height):
                    for i in range(list_width):
                        if(list_main[j][i] == 2):
                            list_main[j][i] = 1
                display_cinema_print.reload()
                save_data()
                return 1
            case 2:
                for j in range(list_height):
                    for i in range(list_width):
                        if(list_main[j][i] == 2):
                            list_main[j][i] = 0
                display_cinema_print.reload()
                return 1
    else:
        print("Ты ЕЩЁ НИЧЕГО НЕ ВЫБРАЛ!!!")

#Подзадача 13
def full_house():
    plase_info_full_house = 0
    for j in range(list_height):
        for i in range(list_width):
            if(list_main[j][i] == 1):
                plase_info_full_house += 1
    if (plase_info_full_house == (list_height*list_width)):
        print("Все  места куплены! Выход из програмы. Хорошего дня!")
        sys.exit(0)

# Подзадача 9
def display_menu():
    print(f"\n{"Меню":^{total_width}}")
    print("1. Обновить таблицу")
    print("2. Выбрать места")
    print("3. Купить места, если есть")
    print("4. Очистить все")
    print("5. Выход")

def display_cinema_reload_and_menu():
        display_cinema_print.reload()
        display_menu()
        switch_menu(only_int(input("Ваш выбор: ")))
    

def switch_menu(x):
    match x:
        case 1:
            display_cinema_reload_and_menu()
        case 2:
            # edit_place.more()
            edit_place_v2()
            display_menu()
            switch_menu(only_int(input("Ваш выбор: ")))
        case 3:
            status_buy = 0
            while status_buy == 0:
                status_buy = buy_place()
            display_menu()
            switch_menu(only_int(input("Ваш выбор: ")))
        case 4:
            mass_init()
            display_cinema_print.reload()
            display_menu()
            switch_menu(only_int(input("Ваш выбор: ")))
        case 5:
            status_exit = only_int(input("Вы точно хотите выйти?\n\t0 - Назад\n\t1 - Выйти из программы\nВвод: "))
            if(status_exit == 1):
                print("Подтвердите выход нажатием клавиши Enter")
                while True:
                    event = keyboard.read_event()
                    if event.event_type ==keyboard.KEY_DOWN:
                        if event.name == 'enter':
                            print("Пока")
                            sys.exit(0)
                        else:
                            display_cinema_reload_and_menu()
                            break
            else:
                display_cinema_reload_and_menu()
mass_init()
display_cinema_print.legend()
display_menu()
full_house()
switch_menu(only_int(input("Ваш выбор: ")))