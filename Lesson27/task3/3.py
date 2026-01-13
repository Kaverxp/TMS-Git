import os

# Создаем директорию
directory_name = 'mydir'
os.makedirs(directory_name, exist_ok=True)

# Сохраняем текущую рабочую директорию
current_dir = os.getcwd()

# Переходим в созданную директорию
os.chdir(directory_name)

# Создаем три пустых файла
for i in range(1, 4):
    filename = f'file{i}.txt'
    with open(filename, 'w') as file:
        pass  # Создаем пустой файл

# Получаем список файлов в директории
files_list = os.listdir()
print(f"Список файлов в директории {directory_name}:")
for file in files_list:
    print(f"  - {file}")

# Возвращаемся в исходную директорию
os.chdir(current_dir)