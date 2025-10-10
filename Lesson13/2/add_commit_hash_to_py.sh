#!/bin/bash

# Добавляет хэш коммита ко всем .py файлам

# Проверяем, находится ли директория в git репозитории
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Ошибка: Текущая директория не является git репозиторием!"
    exit 1
fi

# Получаем короткий хэш коммита
commit_hash=$(git rev-parse --short HEAD)

for file in *.py; do
    if [ -f "$file" ]; then
        # Получаем имя файла без расширения
        filename="${file%.py}"
        
        # Формируем новое имя файла
        new_name="${filename}_${commit_hash}.py"
        
        # Переименовываем файл
        mv "$file" "$new_name"
        
        echo "Переименован: $file -> $new_name"
    fi
done

echo "Готово! Все .py файлы обновлены с хэшем коммита: $commit_hash"