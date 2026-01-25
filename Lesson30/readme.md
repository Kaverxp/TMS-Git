Jenkins Pipeline для задания 30
Описание
Проект с Jenkins Pipeline для автоматизации сборки, тестирования, развертывания и генерации отчетов. Jenkins развернут на Windows с использованием Docker Desktop.

Окружение
ОС: Windows с Docker Desktop

Jenkins: Развернут в Docker контейнере

Docker: Docker Desktop для Windows

Версия Docker: 29.1.3

Версия Python: 3.13.5

Структура
Jenkinsfile - основной Pipeline

deploy.groovy - скрипт для Docker деплоя

report_dsl.py - генератор отчетов


Этапы Pipeline
Initialize - инициализация

Checkout - клонирование репозитория

Build - проверка файлов

Test - запуск тестов

Report - генерация отчетов

Deploy - деплой Docker

Verify - проверка развертывания

Технологии
Jenkins в Docker контейнере

Groovy для Pipeline

Docker Desktop для Windows

Python для отчетов

Nginx в контейнере

Docker на Windows
Проект использует Docker Desktop для Windows с WSL2 бэкендом.
Создается простой веб-сервер на Nginx:

dockerfile
FROM nginx:alpine
RUN echo 'Hello from Jenkins Pipeline on Windows' > /usr/share/nginx/html/index.html
Контейнер запускается на порту 9090.

Особенности Windows
Jenkins запущен в Docker контейнере

Docker Desktop управляет контейнерами через WSL2

Порт 9090 используется для избежания конфликтов с Jenkins (8080)

Все команды выполняются внутри Docker контейнеров

Запуск
Запустить Docker Desktop на Windows

Создать Pipeline Job в Jenkins

Указать репозиторий: https://github.com/Kaverxp/TMS-Git.git

Указать путь: Lesson30/Jenkinsfile

Запустить сборку

Результат
При успешном выполнении:

Docker контейнер запущен на порту 9090

Отчеты сгенерированы в формате JSON

Артефакты заархивированы в Jenkins

Проблемы и решения на Windows
Порт 8080 занят Jenkins - используем порт 9090

Сетевые настройки Docker - контейнеры доступны через localhost

Интеграция WSL2 и Docker - автоматическая настройка через Docker Desktop