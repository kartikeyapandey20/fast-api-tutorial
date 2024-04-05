# This code is for learning purposes and is unrelated to the main codebase.

def add(num1: int, num2: int):
    """Add two numbers together."""
    return num1 + num2

class BankAccount:
    def __init__(self, starting_balance=0):
        """
        Initialize a bank account with an optional starting balance.

        Args:
            starting_balance (int, optional): Starting balance of the bank account. Defaults to 0.
        """
        self.balance = starting_balance

    def deposit(self, amount):
        """
        Deposit money into the bank account.

        Args:
            amount (int): Amount to deposit.
        """
        self.balance += amount
        
    def withdraw(self, amount):
        """
        Withdraw money from the bank account.

        Args:
            amount (int): Amount to withdraw.

        Raises:
            Exception: If the withdrawal amount exceeds the account balance.
        """
        if self.balance < amount:
            raise Exception("Insufficient funds in account")
        self.balance -= amount
        
    def collect_interest(self):
        """Collect interest on the bank account balance."""
        self.balance *= 1.1
