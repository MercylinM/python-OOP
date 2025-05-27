class Account:
    def __init__(self, name):
        self.name = name
        self.deposits = []
        self.withdrawals = []
        self.users = []
        self.balance = 0
        self.loan = 0
        self.frozen = False
        self.min_balance = 0
        self.closed = False

    def deposit(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        if amount > 0:
            self.deposits.append(amount)
            self.balance += amount
            return f"Deposit successful. New balance is {self.balance}"
        return "Deposit amount must be positive."

    def withdraw(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.balance - amount < self.min_balance:
            return "Insufficient funds due to minimum balance requirement."
        if self.balance >= amount:
            self.withdrawals.append(amount)
            self.balance -= amount
            return f"Withdrawal successful. New balance is {self.balance}"
        return "Insufficient funds."

    def transfer_funds(self, amount, other_account):
        if self.closed or self.frozen or other_account.closed or other_account.frozen:
            return "One of the accounts is not active."
        if amount > 0 and self.balance - amount >= self.min_balance and other_account is not None:
            self.users.append(other_account)
            self.balance -= amount
            self.withdrawals.append(amount)
            other_account.balance += amount
            other_account.deposits.append(amount)
            return f"Transfer successful. {other_account.name} will recieve Ksh{amount}. Your new balance is {self.balance}"
        return "Transfer failed due to insufficient funds or invalid amount."

    def get_balance(self):
        return f'Your account balance is {sum(self.deposits) - sum(self.withdrawals)}'

    def request_loan(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        if amount > 0:
            self.loan += amount
            self.balance += amount
            self.deposits.append(amount)
            return f"Loan of {amount} approved. New balance is {self.balance}"
        return "Loan amount must be positive."

    def repay_loan(self, amount):
        if self.closed or self.frozen:
            return "Account is not active."
        if amount > 0:
            if self.balance >= amount:
                if amount > self.loan:
                    self.loan = 0
                    self.deposits += (amount - self.loan)
                    return "Loan fully repaid. Excess deposited to your account."
                self.loan -= amount
                self.balance -= amount
                return f"Loan repayment successful. Remaining loan is {self.loan}"
            return "Insufficient balance."
        return "Repayment amount must be positive."

    def view_account_details(self):
        return f"name: {self.name} \n Balance: {self.balance} \n Loan: {self.loan}"

    def change_account_name(self, new_name):
        if self.closed:
            return "Account is closed."
        self.name = new_name
        return f"name updated to {self.name}"

    def account_statement(self):
        print("Account Statement:")
        for i, deposit in enumerate(self.deposits):
            print(f"Deposit {i+1}: {deposit}")
        for i, withdrawal in enumerate(self.withdrawals):
            print(f"Withdrawal {i+1}: {withdrawal}")

    def apply_interest(self):
        if self.closed or self.frozen:
            return "Account is not active."
        interest = self.balance * 0.05
        self.balance += interest
        self.deposits.append(interest)
        return f"Interest of {interest:.2f} applied. New balance is {self.balance:.2f}"

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
        return "Minimum balance must be non-negative."

    def close_account(self):
        self.closed = True
        self.balance = 0
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        return "Account has been closed and all data reset."
