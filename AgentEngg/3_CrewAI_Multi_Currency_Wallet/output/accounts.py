class Account:
    def __init__(self, initial_usd=0.0) -> None:
        self.balances = {'USD': initial_usd, 'EUR': 0.0, 'GBP': 0.0, 'CAD': 0.0}
        self.transaction_ledger = []

    def create_pocket(self, currency: str, initial_amount: float = 0.0) -> bool:
        if currency not in self.balances:
            return False
        if self.balances[currency] > 0:
            return False
        self.balances[currency] = initial_amount
        return True

    def deposit_usd(self, amount: float) -> None:
        if amount > 0:
            self.balances['USD'] += amount
            self.add_transaction("Deposit", amount, 'USD')

    def exchange_currency(self, from_currency: str, to_currency: str, amount: float, exchange_rate: float) -> bool:
        if self.balances[from_currency] >= amount:
            self.balances[from_currency] -= amount
            amount_converted = amount * exchange_rate
            self.balances[to_currency] += amount_converted
            self.add_transaction(f"Exchange from {from_currency} to {to_currency}", amount, from_currency)
            return True
        return False

    def record_expense(self, currency: str, amount: float) -> bool:
        if self.balances[currency] >= amount:
            self.balances[currency] -= amount
            self.add_transaction("Expense", amount, currency)
            return True
        return False

    def calculate_net_worth(self, get_exchange_rate: callable) -> float:
        total_net_worth = self.balances['USD']
        for currency in ['EUR', 'GBP', 'CAD']:
            rate = get_exchange_rate(currency, 'USD')
            total_net_worth += self.balances[currency] * rate
        return total_net_worth

    def add_transaction(self, description: str, amount: float, currency: str) -> None:
        self.transaction_ledger.append({'description': description, 'amount': amount, 'currency': currency})

    def get_transaction_ledger(self) -> list:
        return self.transaction_ledger