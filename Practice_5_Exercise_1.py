import os

list_main = []
list_width = 16
list_height = 12
tab = 4
tab_mass = 4
#общая ширина + заголовок
total_width = (tab+1) + (list_width*tab_mass)

#Подзадача 1
#Подзадача 9
def mass_init():
    for i in range(list_height):
        temp = ["0"] * list_width
        list_main.append(temp)

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
        print()

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

def edit_place():
    x,y = get_edit_place()
    list_main[y][x] = 2
    display_cinema_print.reload()
# Подзадача 5
#Вспомогательная функция
def edit_place_more():
    x,y = get_edit_place()
    
    free_space = list_width-x # текущая ширина - текущая координата
    
    print(f"Доступно {free_space} мест в данном ряду.")
    more_place = only_int(input("Количество мест: "))
    # Максимальное расстояние до конца
    while more_place <= 0:
        print(f"Ошибка, число больше нуля")
        more_place = only_int(input("Введите корректное количество мест: "))

    #подзадача 6
    skip = 0
    #если вышли за границу то
    if more_place>(free_space):
        print(f"Ошибка, от текущего места {x+1} ряд, {y+1} место. Доступно {free_space} мест.")
        print("Перенос на следующую строку")

        temp = more_place
        # print(range(y, list_height))
        # print(range(x, list_width))
        
        for j in range(y, list_height):
            if(temp <= 0): break #cчетчик 
            if(j == y): #если это ряд начала, тогда идем до конца а потом норм цикл
                for i in range(x, list_width):
                    #Подзадача 10
                    if(list_main[j][i] == 1):
                        print(f"Элемент {j+1} ряд {i+1} место уже куплен")
                        skip += 1
                    else:
                        list_main[j][i] = 2
                        temp -= 1
                    
            else:
                for i in range(list_width):
                    #Подзадача 10
                    if(list_main[j][i] == 1):
                        print(f"Элемент {j+1} ряд {i+1} место уже куплен")
                        skip += 1
                    else:
                        list_main[j][i] = 2
                        temp -= 1
                    if(temp <= 0): break
                    if( j == list_height and i == list_width): break
        

        #Часть 7
        #если достигли конца, но темп еще не ноль, идем с начала до тех пор
        #пока не наступим себе на хвост
        if(temp > 0):
            for j in range(list_height):
                if(temp <= 0): break #cчетчик 
                for i in range(list_width):
                    if(j == y and i == x):
                        print("Ураборос!!")
                        break
                    if(temp <= 0): break #cчетчик 
                    #Подзадача 10
                    if(list_main[j][i] == 1):
                        print(f"Элемент {j+1} ряд {i+1} место уже куплен")
                        skip += 1
                    else:
                        list_main[j][i] = 2
                        temp -= 1
                    
    else:
        for i in range(more_place):
            #Подзадача 10
            if(list_main[y][x+i] == 1):
                print(f"Элемент {y+1} ряд {i+1} место уже куплен")
                skip += 1
                i -= 1 #АХАХАХААХ
            else:
                list_main[y][x+i] = 2  
    print(f"Пропущено {skip}")
    display_cinema_print()
edit_place.more = edit_place_more

# Подзадача 8
def buy_place():
    # Подзадача 9 проверка, есть ли вообще выбранные места
    check_mass_for_2_value = 0
    for j in range(list_height):
                for i in range(list_width):
                    if list_main[j][i] == 2: check_mass_for_2_value += 1
    
    if(check_mass_for_2_value > 0):
        choose = only_int(input("Вы действительно хотите купить билеты?\n\t1-Да\n\t2-Нет (очистить всe)\nВведите: "))
        match choose:
            case 1:
                for j in range(list_height):
                    for i in range(list_width):
                        if(list_main[j][i] == 2):
                            list_main[j][i] = 1
                display_cinema_print.reload()
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
# Подзадача 9
def display_menu():
    print(f"\n{"Меню":^{total_width}}")
    print("1. Обновить таблицу")
    print("2. Выбрать места")
    print("3. Купить места, если есть")
    print("4. Очистить все")

    

def switch_menu(x):
    match x:
        case 1:
            display_cinema_print.reload()
            display_menu()
            switch_menu(only_int(input("Ваш выбор: ")))
        case 2:
            edit_place.more()
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
    
        
mass_init()
display_cinema_print.legend()
display_menu()
switch_menu(only_int(input("Ваш выбор: ")))
