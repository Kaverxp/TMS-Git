# task2.py
# Запись в файл
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write("Это тестовый файл для домашнего задания по программированию")

# Чтение из файла
with open('test.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print("Содержимое файла:")
    print(content)