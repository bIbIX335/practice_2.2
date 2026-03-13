import requests

urls = ["https://github.com/",
        "https://www.binance.com/en",
        "https://tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
        "https://moodle.tomtit-tomsk.ru/"]

for url in urls:
    try:
        response = requests.get(url, timeout = 5)
        code = response.status_code
        if code == 200:
                status = "доступен"
        elif code == 403:
            status = "вход запрещен"
        elif code == 404:
            status = "не найден"
        elif code == 202:
            status = "принято, обработка не завершена"
        elif code >= 500:
            status = "ошибка сервера"
        else:
            status = f"код {code}"

    except requests.exceptions.ConnectionError:
        status = "не доступен"
        code = "-"
    except requests.exceptions.Timeout:
        status = "таймаут"
        code = "-"
    except Exception:
        status = "ошибка"
        code = "-"

    print(f"{url} - {status} - {code}")