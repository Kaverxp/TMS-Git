#!/bin/bash

# Скрипт для замены расширения файла
# Использование: ./script.sh <filename> <new_extension>

# Проверка количества аргументов
if [ $# -ne 2 ]; then
    echo "Ошибка: Необходимо указать два аргумента"
    echo "Использование: $0 <имя_файла> <новое_расширение>"
    echo "Пример: $0 document.txt pdf"
    exit 1
fi

filename="$1"
new_extension="$2"

# Проверка существования файла
if [ ! -f "$filename" ]; then
    echo "Ошибка: Файл '$filename' не существует"
    exit 1
fi

# Извлечение имени файла без расширения
base_name="${filename%.*}"

# Формирование нового имени файла
new_filename="${base_name}.${new_extension}"

# Переименование файла
mv -- "$filename" "$new_filename"

echo "Файл переименован: '$filename' -> '$new_filename'"