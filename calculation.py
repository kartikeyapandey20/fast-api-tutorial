def add(num1 : int, num2 : int):
    return num1 + num2

      
class BankAccount:
    def __init__(self, staring_balance = 0):
        self.balance = staring_balance

    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        if self.balance < amount:
            raise Exception("Insufficient funds in account")
        self.balance -= amount
        
    def collect_interest(self):
        self.balance *= 1.1
