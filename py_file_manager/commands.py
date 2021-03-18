import os
import shutil
import pathlib

class Processing_of_Files: # класс обработчика файлов
    def __init__(self):
        self.sep = os.sep # разделитель, используемый нашей ОС для написания пути к файлам
        self.main_dir = "main_dir" # текущая рабочая директория

    def file_path(self, file_name): # возвращает абсолютный путь к создаваемому файлу или папке
        new_path = self.main_dir + self.sep + file_name
        total_path = pathlib.Path(__file__).parent.absolute() # полный путь к папке, в которой находится наша "корневая" директория
        return str(total_path) + self.sep + new_path

    def command_list(): # список всех доступных комманд
        command_dict = {
            "mkdir": "Создать директорию",
            "rmdir": "Удалить директорию",
            "cd": "Перемещение",
            "ls": "Вывод содержимого директории",
            "create": "Создать файл",
            "write": "Запись в файл",
            "read": "Чтение файла",
            "remove": "Удалить файл",
            "move": "Переместить файл",
            "rename": "Переименовать файл или директорию",
            "help": "Вывести полный список команд"}
        return command_dict

    def help(self): # вывод списка всех доступных комманд
        print('\n==== Список доступных команд: ====')
        print("""mkdir -- Создать директорию
rmdir -- Удалить директорию
cd -- Перемещение
ls -- Вывод содержимого директории
create -- Создать файл
write -- Запись в файл
read -- Чтение файла
remove -- Удалить файл
move -- Переместить файл
rename -- Переименовать директорию
help -- Вывести полный список команд
====================================""")

    def translate(self, command): # связываем команды, вводимые пользователем, с методами класса
        commands = [ self.mkdir,
            self.rmdir,
            self.cd,
            self.ls,
            self.create,
            self.write,
            self.read,
            self.remove,
            self.move,
            self.rename,
            self.help ]
        commands = dict(zip(Processing_of_Files.command_list().keys(), commands))
        return commands.get(command)

    def mkdir(self, dir_name): # создать папку
        new_dir_path = self.file_path(dir_name)
        try:
            os.mkdir(new_dir_path)
        except FileExistsError:
            print("Такая директория уже существует.")

    def rmdir(self, dir_name): # удалить папку
        rm_dir_path = self.file_path(dir_name)
        try:
            os.rmdir(rm_dir_path)
        except FileNotFoundError:
            print("Такой папки не существует.")
        except NotADirectoryError:
            print(f"{dir_name} не является папкой.")
        except OSError: # в случае если папка не пустая
            try:
                shutil.rmtree(rm_dir_path, ignore_errors=False) # удаляем, игнорируя сообщения об ошибке
            except FileNotFoundError:
                print("Такой папки не существует.")
            except NotADirectoryError:
                print(f"{dir_name} не является папкой.")

    def cd(self, dir_name): # перемещение по папкам
        if dir_name == ".." and self.main_dir.find(self.sep) != -1: # просто переходим наверх
            self.main_dir = self.main_dir[:self.main_dir.rfind(self.sep)]
            new_dir_path = str(pathlib.Path(__file__).parent.absolute()) + self.sep + self.main_dir
        elif dir_name == "..": # пытаемся выйти за нашу "корневую" папку
            print("Вы достигли корневой папки.")
            new_dir_path = str(pathlib.Path(__file__).parent.absolute()) + self.sep + self.main_dir
        else: # просто переходим в папку по названию
            new_dir_path = self.file_path(dir_name)
            self.main_dir += self.sep + dir_name

        # print(new_dir_path)
        # print(self.main_dir)
        try:
            os.chdir(new_dir_path)
        except FileNotFoundError:
            print("Такой папки не существует.")
        except NotADirectoryError:
            print(f"{dir_name} не является директорией.")

    def ls(self): # вывод содержимого текущей директории
        total_dir_path = str(pathlib.Path(__file__).parent.absolute()) + self.sep + self.main_dir
        file_list = os.listdir(total_dir_path)
        # print(file_list)
        if len(file_list) > 0:
            for i in range(len(file_list)):
                if os.path.isdir(self.file_path(file_list[i])):
                    print(f"[{file_list[i]}]")
                elif os.path.isfile(self.file_path(file_list[i])):
                    print(f"{file_list[i]}")
        else:
            print("Это пустая директория.")

    def create(self, file_name): # создать файла
        new_file_path = self.file_path(file_name)
        if not os.path.exists(new_file_path):
            try:
                open(new_file_path, "a+").close()
            except IsADirectoryError:
                print(f"Уже существует директория с тем же именем.")
        else:
            print("Файл с таким именем уже существует.")

    def write(self, file_name, *text): # записать в файл
        file_path = self.file_path(file_name)
        text = " ".join(text)
        mode = 'a' if os.path.exists(file_path) else 'w'
        try:
            with open(file_path, mode) as file:
                file.write(text)
        except IsADirectoryError:
            print("Это директория.")

    def read(self, file_name) -> str: # прочесть файл
        file_path = self.file_path(file_name)
        try:
            with open(file_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print("Файл не найден.")
        except IsADirectoryError:
            print("Это директория.")

    def remove(self, file_name: str): # удалить файл
        file_path = self.file_path(file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print("Такого файла нет.")

    def rename(self, old_name, new_name): # переименовать файл
        old_path = self.file_path(old_name)
        new_path = self.file_path(new_name)
        try:
            if not os.path.isfile(new_path):
                os.rename(old_path, new_path)
            else:
                raise IsADirectoryError
        except FileNotFoundError:
            print("Нет такого файла.")
        except IsADirectoryError:
            print("Файл с таким названием уже есть.")

    def move(self, file_name, path): # переместить файл
        old_path = self.file_path(file_name)
        if ".." in path: # на уровень выше
            new_path = self.main_dir[:self.main_dir.rfind(os.sep)] + self.sep + file_name
        else:
            if os.path.isdir(self.file_path(path)): # это директория
                new_path = self.file_path(path + self.sep + file_name)
        try:
            shutil.move(old_path, new_path)
        except FileNotFoundError:
            print("Файл не найден.")
