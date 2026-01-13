class BankAccount:
    def __init__(self, number, name, balance=0):
        self.number = number
        self.name = name
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return self.balance
        return "Insufficient funds"

acc1 = BankAccount("2026", "Test1", 1000)
acc2 = BankAccount("7570", "Test2")

print(f"Account {acc1.number}: {acc1.name}")
print(f"Balance: {acc1.balance}")
print(f"After deposit 500: {acc1.deposit(500)}")
print(f"After withdraw 300: {acc1.withdraw(300)}")

print(f"\nAccount {acc2.number}: {acc2.name}")
print(f"Balance: {acc2.balance}")
print(f"Deposit 1000: {acc2.deposit(1000)}")
print(f"Try to withdraw 1500: {acc2.withdraw(1500)}")