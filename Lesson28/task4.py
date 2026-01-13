class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_year(self):
        return self.year
    
    def set_title(self, new_title):
        self.title = new_title
    
    def set_author(self, new_author):
        self.author = new_author
    
    def set_year(self, new_year):
        self.year = new_year

b1 = Book("Book1", "Author1", 2000)
b2 = Book("Book2", "Author2", 2010)

print(f"Book 1: {b1.get_title()}, {b1.get_author()}, {b1.get_year()}")
print(f"Book 2: {b2.get_title()}, {b2.get_author()}, {b2.get_year()}")

b1.set_title("New Book 1")
b2.set_year(2020)

print(f"\nAfter changes:")
print(f"Book 1: {b1.get_title()}, {b1.get_author()}, {b1.get_year()}")
print(f"Book 2: {b2.get_title()}, {b2.get_author()}, {b2.get_year()}")