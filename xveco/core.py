class Currency:
    def __init__(self, name, symbol, value_to_eur, logo=None):
        self.name = name
        self.symbol = symbol
        self.value_to_eur = value_to_eur
        self.logo = logo
        self.accounts = []

    def apply_inflation(self, percent):
        self.value_to_eur *= (1 + percent / 100)


class Account:
    def __init__(self, name, currency):
        self.name = name
        self.currency = currency
        self.balance = 0  # céntimos
        self.debts = []

        self.currency.accounts.append(self)

    def deposit(self, amount):
        self.balance += int(amount * 100)

    def withdraw(self, amount):
        cents = int(amount * 100)

        if cents > self.balance:
            raise ValueError("no tienes suficiente saldo")

        self.balance -= cents

    def transfer(self, other_account, amount):
        cents = int(amount * 100)

        if cents <= 0:
            raise ValueError("cantidad inválida")

        self.withdraw(amount)
        other_account.deposit(amount)

    def balance_in_eur(self):
        return self.balance / 100 * self.currency.value_to_eur

    def show_balance(self):
        euros = self.balance / 100
        logo = self.currency.logo or ""
        print(f"{logo} {self.name}: {euros:,.2f} {self.currency.symbol}"
              .replace(",", "X").replace(".", ",").replace("X", "."))


class Bank:
    def __init__(self, currency, supply):
        self.currency = currency
        self.supply = int(supply * 100)

    def loan(self, account, amount, interest):
        cents = int(amount * 100)

        if cents > self.supply:
            raise ValueError("el banco no tiene suficiente dinero")

        self.supply -= cents
        account.balance += cents

        account.debts.append({
            "amount": cents,
            "interest": interest
        })

    def calculate_debt(self, account):
        total = 0

        for d in account.debts:
            total += int(d["amount"] * (1 + d["interest"] / 100))

        return total

    def pay_debt(self, account):
        total = self.calculate_debt(account)

        if account.balance < total:
            raise ValueError("no puedes pagar la deuda")

        account.balance -= total
        account.debts.clear()