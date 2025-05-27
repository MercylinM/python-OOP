class Student:
    name = "Mercy"
    age = 20
    country = "Kenya"
    school = "AkiraChix"

class Student1:
    school = "AkiraChix"
    def __init__(self, first_name, last_name, age, country):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.country = country
        self.year = 2025 - age
        self.scores = []

    def greet_student(self):
        return f'Hello {self.first_name}, welcome to {self.school}'
    
    def initials(self):
        return self.first_name[0] + self.last_name[0]
    
    def add_score(self, score):
        self.scores.append(score)
        total = 0
        for s in self.scores:
            total += s
        return f'your new total is {total}'