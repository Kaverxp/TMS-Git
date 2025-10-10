#!/bin/bash

# Добавляет timestamp ко всем .log файлам в формате filename_{timestamp}.log

for file in *.log; do
    if [ -f "$file" ]; then
        # Получаем имя файла без расширения
        filename="${file%.log}"
        
        # Генерируем timestamp
        timestamp=$(date +%Y%m%d_%H%M%S)
        
        # Формируем новое имя файла
        new_name="${filename}_${timestamp}.log"
        
        # Переименовываем файл
        mv "$file" "$new_name"
        
        echo "Переименован: $file -> $new_name"
    fi
done

echo "Готово! Все .log файлы обновлены с timestamp."