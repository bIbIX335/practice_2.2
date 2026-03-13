import requests
import json

user = None
repos = None
discus = None

def select_user():
    login = input("Введите логин пользователя: ")
    global user
    user = requests.get(f"https://api.github.com/users/{login}")
    if user.status_code == 404:
        print("Пользователь не найден")
        user = None
    elif user.status_code == 200:
        user = user.json()
        global repos
        repos = requests.get(f"https://api.github.com/users/{login}/repos")
        global discus
        discus = requests.get(f"https://api.github.com/search/issues?q=author:{login}+type:discussion")
        print(f"Пользователь {login} выбран")
    else:
        print(f"Неизвестный код ответа {user.status_code}")
        user = None

def show_profile():
    if user is not None:
        print(f"====={user["login"]}=====")

        if user["name"] is None: name = "Не указано"
        else: name = user["name"]

        if discus.status_code == 200: dis_col = discus.json()["total_count"]
        else: dis_col = "[ОШИБКА ПРИ ПОЛУЧЕНИИ ДАННЫХ]"
        
        print(f"Имя: {name}")
        print(f"Ссылка на профиль: https://github.com/{user["login"]}")
        print(f"Публичных репозиториев: {user["public_repos"]}")
        print(f"Обсуждений: {dis_col}")
        print(f"Подписок: {user["following"]}")
        print(f"Подписчиков: {user["followers"]}")
    else:
        print("Пользователь не выбран")

def print_repo(repo):
    print(f"\nНазвание: {repo["name"]}")
    print(f"Ссылка: {repo["html_url"]}")
    print(f"Наблюдателей (watchers): {repo["watchers_count"]}")
    print(f"Язык: {repo["language"]}")
    print(f"Видимость: {repo["visibility"]}")
    print(f"Ветка по умолчанию: {repo["default_branch"]}")

def show_all_repos():
    if user is not None:
        repos1 = repos.json()
        if len(repos1) > 0:
            for repo in repos1:
                print_repo(repo)
        else:
            print("У пользователя нет репозиториев")
    else:
        print("Пользователь не выбран")

def show_repo():
    if user is not None:
        repo_name = input("Введите название репозитория: ").strip()
        if repo_name:
            for repo in repos.json():
                if repo_name == repo["name"]:
                    print_repo(repo)
                    return
            print("Такой репозиторий не найден")
        else:
            print("Название не должно быть пустым")
    else:
        print("Пользователь не выбран")

while True:
    print("1) Выбрать пользователя")
    print("2) Просмотреть профиль пользователя")
    print("3) Просмотреть все репозитории пользователя")
    print("4) Просмотреть конкретный репозиторий")
    print("0) Выход")

    choice = input("Выберите действие: ")

    match choice:
        case "1":
            select_user()
        case "2":
            show_profile()
        case "3":
            show_all_repos()
        case "4":
            show_repo()
        case "0":
            print("Всего доброго!")
            break
        case _:
            print("Недоступная команда")