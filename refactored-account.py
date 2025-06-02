from datetime import datetime


class Transaction:
    def __init__(self, narration, amount, transaction_type):
        self.timestamp = datetime.now()
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type  



class Account:
    def __init__(self, name, number):
        self.name = name
        self.__balance = 0
        self.__account_number = number
        self.loan = 0
        self.frozen = False
        self.min_balance = 0
        self.closed = False
        self.users = []
        self.transactions = []


    def __log_transaction(self, narration, amount, transaction_type):
        transaction = Transaction(narration, amount, transaction_type)
        self.transactions.append(transaction)


    def deposit(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        elif amount > 0:
            self.__balance += amount
            self.__log_transaction("Deposit", amount, "deposit")
            return f"Deposit successful. New balance is {self.get_balance()}"
        else:
            return "Deposit amount must be positive."


    def withdraw(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        elif amount <= 0:
            return "Withdrawal amount must be positive."
        elif self.__balance - amount < self.min_balance:
            return "Insufficient funds due to minimum balance requirement."
        elif self.__balance >= amount:
            self.__balance -= amount
            self.__log_transaction("Withdrawal", amount, "withdrawal")
            return f"Withdrawal successful. New balance is {self.get_balance()}"
        else:
            return "Insufficient funds."


    def transfer_funds(self, amount, other_account):
        if not isinstance(other_account, Account):
            return "Incompatible recipient"
        if self.closed or self.frozen or other_account.closed or other_account.frozen:
            return "One of the accounts is not active."
        elif amount > 0 and self.__balance - amount >= self.min_balance:
            self.__balance -= amount
            self.__log_transaction(f"Transfer to {other_account.name}", amount, "transfer")
            other_account.receive_transfer(amount, self.name)
            return f"Transfer successful. {other_account.name} received Ksh{amount}. Your new balance is {self.get_balance()}"
        else:
            return "Transfer failed due to insufficient funds or invalid amount."


    def receive_transfer(self, amount, sender_name):
        self.__balance += amount
        self.__log_transaction(f"Transfer from {sender_name}", amount, "transfer")


    def get_balance(self):
        return self.__balance


    def request_loan(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        elif amount > 0:
            self.loan += amount
            self.__balance += amount
            self.__log_transaction("Loan approved", amount, "loan")
            return f"Loan of {amount} approved. New balance is {self.get_balance()}"
        else:
            return "Loan amount must be positive."


    def repay_loan(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        elif amount <= 0:
            return "Repayment amount must be positive."
        if self.__balance < amount:
            return "Insufficient balance."
        if amount >= self.loan:
            excess = amount - self.loan
            self.__balance -= amount
            self.loan = 0
            self.__log_transaction("Loan repaid", amount, "repayment")
            if excess > 0:
                self.__balance += excess
                self.__log_transaction("Excess after loan repayment", excess, "deposit")
            return "Loan fully repaid."
        else:
            self.__balance -= amount
            self.loan -= amount
            self.__log_transaction("Partial loan repayment", amount, "repayment")
            return f"Loan repayment successful. Remaining loan is {self.loan}"


    def view_account_details(self):
        return f"Name: {self.name} \nBalance: {self.get_balance()} \nLoan: {self.loan}"


    def change_account_name(self, new_name):
        if self.closed:
            return "Account is closed."
        else:
            self.name = new_name
            return f"Name updated to {self.name}"


    def account_statement(self):
        print("Account Statement:")
        for transaction in self.transactions:
            print(transaction)


    def apply_interest(self):
        if self.closed or self.frozen:
            return "Account is not active."
        else:
            interest = self.__balance * 0.05
            self.__balance += interest
            self.__log_transaction("Interest Applied", interest, "deposit")
            return f"Interest of {interest:.2f} applied. New balance is {self.get_balance():.2f}"


    def freeze_account(self):
        self.frozen = True
        return "Account has been frozen."


    def unfreeze_account(self):
        self.frozen = False
        return "Account has been unfrozen."


    def set_minimum_balance(self, amount):
        if amount >= 0:
            self.min_balance = amount
            return f"Minimum balance set to {amount}"
        else:
            return "Minimum balance must be non-negative."


    def close_account(self):
        self.closed = True
        self.__balance = 0
        self.loan = 0
        self.transactions.clear()
        return "Account has been closed and all data reset."

