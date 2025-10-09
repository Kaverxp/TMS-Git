#!/bin/bash

# Проверка количества аргументов
if [ $# -ne 3 ]; then
    echo "Ошибка: Необходимо указать 3 аргумента:"
    echo "Использование: $0 <выходной_файл> <каталог> <расширение>"
    echo "Пример: $0 result.txt /home/user/docs txt"
    exit 1
fi

output_file="$1"
directory="$2"
extension="$3"

# Проверка существования каталога
if [ ! -d "$directory" ]; then
    echo "Ошибка: Каталог '$directory' не существует или не является каталогом"
    exit 1
fi

# Удаляем точку из расширения, если пользователь её указал
extension="${extension#.}"

# Очищаем файл вывода или создаем новый
> "$output_file"

# Поиск файлов с заданным расширением и запись в файл
echo "=== Файлы с расширением .$extension в каталоге $directory ===" > "$output_file"
echo "Найдено файлов: $(find "$directory" -maxdepth 1 -type f -name "*.$extension" | wc -l)" >> "$output_file"
echo "Список файлов:" >> "$output_file"
echo "----------------------------------------" >> "$output_file"

# Записываем имена файлов
find "$directory" -maxdepth 1 -type f -name "*.$extension" -printf "%f\n" >> "$output_file"

# Вывод информации пользователю
echo "Результат записан в файл: $output_file"
echo "Найдено файлов с расширением .$extension: $(find "$directory" -maxdepth 1 -type f -name "*.$extension" | wc -l)"
