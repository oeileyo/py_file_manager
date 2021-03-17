from path import *
from commands import *

def main():
    file_processing = Processing_of_Files() # создаем объект класса обработчик файлов
    file_processing.help()

    while True:
        command = input("\n>>").split(" ")
        if command[0] == "exit":
            print("\nВы завершили работу программы.")
            break

        result = file_processing.translate(command[0]) # проверка на существование такой команды в нашем файловом менеджере (T/F)
        if result:
            result(*command[1:])
        else:
            print(f"\nТакой команды не существует. Для ознакомления со списком команд введите \"help\".")

main()