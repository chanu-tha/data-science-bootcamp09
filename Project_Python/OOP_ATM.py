from random import randint
import numpy as np

class ATM:
    pass
  
class ATM():
    def __init__(self, account_name, bank_name, initial):
        self.account_name = account_name
        self.bank_name = bank_name
        self.balance = initial

    # Bank account info
    def __str__(self):
        return f"This is an account of {self.account_name}, bank: {self.bank_name}."
    
    # Check balance
    def check_balance(self):
        print(f"Your current balance: {self.balance}.")
    
    # Withdraw money
    def withdraw(self, money_w):
        if money_w > self.balance:
            print("Insufficent fund. Try it again.")
        else:
            self.balance -= money_w
            print(f"Withdraw succesful. Your balance is {self.balance}.")
            print("Please receive the money. Thank you.")
          
    # Deposit Money 
    def deposit(self, money_d):
        self.inni_balance += money_d
        print(f"Deposit successful. Your balance is {self.balance}.")
        print("Thank you.")
      
    # Transfer Money
    def transfer(self, money_t, recipient):
        if money_t > self.balance:
            print("Insufficent fund. Try it again.")
        else:
            self.balance -= money_t
            print(f"You transfer to {recipient} is success. Your balance is {self.balance}.")
            print("Thank you.")
          
    # Pay water bill
    def pay_water_bill(self, money_bill):
        if money_bill > self.balance:
            print("Insufficent fund. Try it again.")
        else:
            self.balance -= money_bill
            print(f"Your water bill has been paid successfully. Your balance is {self.balance}.")

    # generate account no.
    def bank_account(self):
        np.random.seed(35)
        first_digit = np.random.randint(1,9, size =1)
        digits = np.random.randint(0,9,size = 9)
        # combine two instances and convert to str
        account_number = ''.join(map(str, np.concatenate([first_digit, digits])))
        return account_number

beam_bank = ATM("beam", "BBL", 1000)

print(beam_bank)
beam_bank.bank_account()

beam_bank.pay_water_bill(450)

beam_bank.check_balance()

