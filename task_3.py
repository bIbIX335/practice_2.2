import requests
import json
from pathlib import Path

path = Path(__file__).parent / "resource" / "save.json"
currencies = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()["Valute"]

def show_currencies(currencies):
    line = "=" * 88
    print(line)
    print("| {:3} | {:30} | {:7} | {:15} | {:13} |".format("Код", "Валюта", "Номинал", "Курс за номинал", "Курс за 1 ед."))
    print(line)

    for code in sorted(currencies.keys()):
        currency = currencies[code]

        print("| {:3} | {:30} | {:7} | {:15.2f} | {:13.2f} |".format(
            currency["CharCode"],
            currency["Name"][:30],
            currency["Nominal"],
            currency["Value"],
            currency["Value"] / currency["Nominal"]
        ))

    print(line)

def show_currency(code):
    if not code in currencies.keys():
        print("Нет валюты с таким кодом")
        return
    
    currency = currencies[code]
    print(f"{code} ({currency["Name"]}):")
    print(f"ID - {currency["ID"]}")
    print(f"Номер - {currency["NumCode"]}")
    print(f"Номинал - {currency["Nominal"]} ед.")
    print(f"Курс за номинал - {currency["Value"]} руб.")
    print(f"Курс за единицу - {currency["Value"] / currency["Nominal"]} руб.")

def create_group(name):
    with open(path, "r", encoding = "utf-8") as file:
        save = json.load(file)
        if name not in save:
            save[name] = {}
            with open(path, "w", encoding = "utf-8") as file:
                json.dump(save, file, ensure_ascii = False, indent = 4)
            print("Группа успешна создана")
        else:
            print("Такая группа уже есть")

def add_cur_to_group():
    pair = input("Введите код валюты и название группы через запятую: ").split(",")
    pair = [x.strip() for x in pair]
    if len(pair) == 2:
        currency, group = pair
        currency = currency.upper()
    else:
        print("Введены неверные данные")
        return
    
    with open(path, "r", encoding = "utf-8") as file:
        save = json.load(file)
        if not group in save:
            print("Нет такой группы")
            return
        if currency in save[group]:
            print("Валюта уже есть в группе")
            return
        elif currency in currencies:
            save[group][currency] = currencies[currency]
            with open(path, "w", encoding = "utf-8") as file:
                json.dump(save, file, ensure_ascii = False, indent = 4)
            print(f"Валюта {currency} добавлена в группу {group}")
        else:
            print("Нет такой валюты")

def delete_cur_from_group():
    pair = input("Введите код валюты и название группы через запятую: ").split(",")
    pair = [x.strip() for x in pair]
    if len(pair) == 2:
        currency, group = pair
        currency = currency.upper()
    else:
        print("Введены неверные данные")
        return
    
    with open(path, "r", encoding = "utf-8") as file:
        save = json.load(file)
        if not group in save:
            print("Нет такой группы")
            return
        if currency in currencies:
            del save[group][currency]
            with open(path, "w", encoding = "utf-8") as file:
                json.dump(save, file, ensure_ascii = False, indent = 4)
            print(f"Валюта {currency} удалена из группы {group}")
        else:
            print("Нет такой валюты")

def show_groups():
    with open(path, "r", encoding = "utf-8") as file:
        save = json.load(file)
        if len(save) == 0:
            print("У вас еще нет групп валют")
            return
        
        for group in save.keys():
            print(f"{group}; валют - {len(save[group])}")

while True:
    try:
        with open(path, "r") as file:
            pass
    except FileNotFoundError:
        with open(path, "w") as file:
            json.dump({}, file)

    print("1) Просмотреть все валюты")
    print("2) Просмотреть конкретную валюту по коду")
    print("3) Создать группу валют")
    print("4) Просмотреть созданные группы")
    print("5) Добавить валюту в группу")
    print("6) Удалить валюту из группы")
    print("7) Просмотреть валюты группы")
    print("0) Выход")

    choice = input("Выберите действие: ")

    match choice:
        case "1":
            show_currencies(currencies)
        case "2":
            currency = input("Введите код валюты: ").upper()
            if currency in currencies:
                show_currency(currency)
            else:
                print("Валюты с таким кодом нет")
        case "3":
            group = input("Введите название группы: ")
            if group:
                create_group(group)
            else:
                print("Название не может быть пустым")
        case "4":
            show_groups()
        case "5":
            add_cur_to_group()
        case "6":
            delete_cur_from_group()
        case "7":
            group = input("Введите название группы: ")
            with open(path, "r", encoding = "utf-8") as file:
                save = json.load(file)
                if group in save:
                    show_currencies(save[group])
                else:
                    print("Нет такой группы")
        case "0":
            print("Всего доброго!")
            break
        case _:
            print("Недоступная команда")