from calculation import add , BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1 , num2 , expected",[
    (3,2,5),
    (3,1,4),
    (3,0,3),
])
def test_add(num1 , num2 , expected):
    sum = add(num1, num2)
    assert sum  == expected

def test_bank_account_zero_balance(zero_bank_account):
    
    assert zero_bank_account.balance == 0
    
    
def test_bank_account_with_initial_amount(bank_account):
    assert bank_account.balance == 50
@pytest.mark.parametrize("deposit, withdraw, expected",[
    (200, 100, 150),
    (50, 10, 90),
    (100, 50, 100),
])
def test_bank_account_deposit(bank_account,deposit, withdraw ,expected):
    bank_account.deposit(deposit)
    bank_account.withdraw(withdraw)
    
    assert bank_account.balance == expected
    
    
def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)