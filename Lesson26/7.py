def find_common_characters(str1, str2):
    """
    Находит символы, которые встречаются в обеих строках.
    """
    # Используем пересечение множеств
    common_chars = set(str1) & set(str2)
    
    print(f"Первая строка: '{str1}'")
    print(f"Вторая строка: '{str2}'")
    print(f"Общие символы: {common_chars}")
    return common_chars

# Пример использования:
find_common_characters("hello", "world")