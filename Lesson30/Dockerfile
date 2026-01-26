# Используем легковесный базовый образ
FROM nginx:alpine

# Устанавливаем метаданные
LABEL maintainer="Student"
LABEL version="1.0"
LABEL description="TMS Application for Jenkins Pipeline"

# Удаляем дефолтную страницу nginx
RUN rm -rf /usr/share/nginx/html/*

# Копируем наши файлы
COPY html/ /usr/share/nginx/html/

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]

# Добавляем health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1