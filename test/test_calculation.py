from calculation import add, BankAccount  # Import the functions/classes to be tested
import pytest

# Define fixtures to create instances of BankAccount with different initial balances
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# Test the add function with various parameters
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (3, 1, 4),
    (3, 0, 3),
])
def test_add(num1, num2, expected):
    sum = add(num1, num2)
    assert sum == expected

# Test the BankAccount class
def test_bank_account_zero_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account_with_initial_amount(bank_account):
    assert bank_account.balance == 50

# Test deposit and withdrawal functionality of BankAccount
@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200, 100, 150),
    (50, 10, 40),
    (100, 50, 100),
])
def test_bank_account_deposit_withdraw(bank_account, deposit, withdraw, expected):
    bank_account.deposit(deposit)
    bank_account.withdraw(withdraw)
    assert bank_account.balance == expected

# Test insufficient funds exception when withdrawing
def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)
