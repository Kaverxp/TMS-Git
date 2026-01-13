class Student:
    def __init__(self, name, age, grades=None):
        self.name = name
        self.age = age
        self.grades = grades or []
    
    def add_grade(self, grade):
        if 2 <= grade <= 5:
            self.grades.append(grade)
    
    def avg_grade(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0
    
    def status(self):
        avg = self.avg_grade()
        if avg >= 4.5:
            return "excellent"
        elif avg >= 3.5:
            return "good"
        else:
            return "average"

s1 = Student("Test1", 20, [5, 5, 4, 5])
s2 = Student("Test2", 21, [4, 3, 4, 3])
s3 = Student("Test3", 19, [3, 2, 3, 3])

s1.add_grade(5)
s2.add_grade(4)
s3.add_grade(2)

students = [s1, s2, s3]

for student in students:
    print(f"\n{student.name}, {student.age} years")
    print(f"Grades: {student.grades}")
    print(f"Average: {student.avg_grade():.2f}")
    print(f"Status: {student.status()}")