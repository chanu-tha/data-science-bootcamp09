# Homework 2

class DataAnalyst:
  def __init__(self, name, position, gender, salary):
    self.name = name
    self.position = position
    self.gender = gender
    self.salary = salary

  def info(self):
    print(f"{self.name} is a {self.position} with {self.salary} salary.")

  # Greeting
  def monday(self):
    if self.gender == M or self.gender == m:
      print(f"Good morning! Mr.{self.name}. Have a great week.")
    else:
      print(f"Good morning! Ms.{self.name}. Have a great week.")

  # Coffee response
  def coffee(self):
    print(f"{self.name} is going out for a coffee.")

employee_01 = DataAnalyst("Salah", "Junior DA", "M", 35500)

employee_01.info()
employee_01.coffee()
