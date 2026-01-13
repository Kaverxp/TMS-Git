from jinja2 import Template
import os

# Чтение шаблона из файла
with open('template.html', 'r', encoding='utf-8') as file:
    template_content = file.read()

# Создаем объект шаблона
template = Template(template_content)

# Создаем список пользователей
users = [
    {"name": "Test1", "email": "test1@example.com"},
    {"name": "Test2", "email": "test2@example.com"},
    {"name": "Test3", "email": "test3@example.com"}
]

# Рендерим шаблон с данными
rendered_html = template.render(users=users)

# Сохраняем результат в HTML файл
with open('users.html', 'w', encoding='utf-8') as file:
    file.write(rendered_html)

print("HTML файл успешно создан: users.html")

# Выводим результат в консоль для проверки
print("\nСписок пользователей:")
for i, user in enumerate(users, 1):
    print(f"{i}. Имя: {user['name']}, Email: {user['email']}")