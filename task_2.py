import psutil
import os

def print_percent_bar(percent):
    n = int(percent / 4)
    print(f"[{"█" * n}{" " * (25 - n)}]")

cpu = psutil.cpu_percent(interval = 1)

try:
    while True:
        print("====УЛЬТРАСУПЕРМЕГАМОНИТОРИНГ====")
        print(f"\nЗагрузка CPU: {cpu}%")
        print_percent_bar(cpu)

        ram = psutil.virtual_memory().percent
        print(f"\nИспользовано оперативной памяти: {ram}%")
        print_percent_bar(ram)

        if os.name == 'nt':
            disk = psutil.disk_usage('C:\\').percent
        else:
            disk = psutil.disk_usage('/').percent
        print(f"\nЗагруженность диска: {disk}%")
        print_percent_bar(disk)

        print("\nCtrl+C для выхода")

        cpu = psutil.cpu_percent(interval = 1.5)

        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
except KeyboardInterrupt:
    print("До свидания")