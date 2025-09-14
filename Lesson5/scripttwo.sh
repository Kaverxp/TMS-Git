#!/bin/bash

# Скрипт для выделения подстроки по порядковым номерам символов
# Использование: ./script.sh "строка" начальный_индекс конечный_индекс

# Проверка количества аргументов
if [ $# -ne 3 ]; then
    echo "Ошибка: Необходимо указать три аргумента"
    echo "Использование: $0 \"строка\" начальный_индекс конечный_индекс"
    echo "Пример: $0 \"Hello World\" 2 7"
    exit 1
fi

original_string="$1"
start_index="$2"
end_index="$3"

# Проверка, что индексы - числа
if ! [[ "$start_index" =~ ^[0-9]+$ ]] || ! [[ "$end_index" =~ ^[0-9]+$ ]]; then
    echo "Ошибка: Индексы должны быть целыми числами"
    exit 1
fi

# Проверка корректности индексов
if [ "$start_index" -gt "$end_index" ]; then
    echo "Ошибка: Начальный индекс не может быть больше конечного"
    exit 1
fi

# Получение длины строки
string_length=${#original_string}

# Проверка выхода за границы строки
if [ "$start_index" -ge "$string_length" ] || [ "$end_index" -ge "$string_length" ]; then
    echo "Ошибка: Индексы выходят за границы строки (длина: $string_length)"
    exit 1
fi

# Выделение подстроки (индексы в bash начинаются с 0)
substring="${original_string:$start_index:$((end_index - start_index + 1))}"

echo "Исходная строка: '$original_string'"
echo "Длина строки: $string_length"
echo "Подстрока с $start_index по $end_index символ: '$substring'"