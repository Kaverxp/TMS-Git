# Jenkins Pipeline для TMS-Git

## Описание
Pipeline для автоматической сборки и развёртывания приложения с использованием Jenkins, Docker и Groovy.

## Структура Pipeline

### Этапы:
1. **Checkout** - Клонирование репозитория Git
2. **Test Groovy Script** - Загрузка и выполнение Groovy скрипта деплоя
3. **Verify Results** - Проверка результатов выполнения

### Параметры:
- `ENVIRONMENT` - Окружение (dev, test)
- `IMAGE_TAG` - Тег Docker образа (по умолчанию: v1.0)

### Groovy скрипт: deploy.groovy
Автоматизирует:
- Создание Dockerfile (если отсутствует)
- Сборку Docker образа
- Остановку и удаление предыдущего контейнера
- Запуск нового контейнера
- Проверку здоровья приложения

## Требования
- Jenkins с Docker Pipeline плагином
- Docker на агенте Jenkins
- Git репозиторий с приложением

## Запуск
1. Создайте Pipeline job в Jenkins
2. Укажите URL репозитория: `https://github.com/Kaverxp/TMS-Git.git`
3. Запустите с параметрами ENVIRONMENT и IMAGE_TAG