from accounts import Account
import gradio as gr

def get_exchange_rate(currency_from, currency_to):
    # 1. Add USD to the dictionary
    rates = {
        'USD': 1.0,
        'EUR': 1.1,  
        'GBP': 1.3,
        'CAD': 0.75,
    }
    
    # 2. Check if both currencies exist to avoid future KeyErrors
    if currency_from not in rates or currency_to not in rates:
        return 1.0 

    # 3. Calculate cross-rate: (Base to USD) / (Target to USD)
    # Example: USD to EUR would be 1.0 / 1.1 = 0.909
    return rates[currency_from] / rates[currency_to]


account = Account()

def create_pocket(currency, initial_amount):
    success = account.create_pocket(currency, initial_amount)
    return f"Pocket created: {success}"

def deposit_usd(amount):
    account.deposit_usd(amount)
    return f"Deposited: ${amount}"

def exchange_currency(from_currency, to_currency, amount):
    rate = get_exchange_rate(from_currency, to_currency)
    success = account.exchange_currency(from_currency, to_currency, amount, rate)
    return f"Exchange successful: {success}"

def record_expense(currency, amount):
    success = account.record_expense(currency, amount)
    return f"Expense recorded: {success}"

def calculate_net_worth():
    net_worth = account.calculate_net_worth(get_exchange_rate)
    return f"Total Net Worth: ${net_worth}"

def get_ledger():
    return account.get_transaction_ledger()

app = gr.Interface(
    fn=lambda currency, amount: create_pocket(currency, amount) if currency else deposit_usd(amount),
    inputs=[
        gr.Dropdown(["USD", "EUR", "GBP", "CAD"], label="Currency for Pocket Creation"),
        gr.Number(label="Initial Amount", value=0.0),
        gr.Number(label="Deposit Amount", value=0.0)
    ],
    outputs="text",
    title="NomadBank - Multi-Currency Wallet",
    description="Demonstrate the NomadBank Wallet Functionality"
)

# 1. Define each feature as a separate interface
# Note: Ensure the function names (deposit_usd, etc.) match exactly what is in your app.py
deposit_ui = gr.Interface(fn=deposit_usd, inputs="number", outputs="text")
exchange_ui = gr.Interface(fn=exchange_currency, inputs=["text", "text", "number"], outputs="text")
expense_ui = gr.Interface(fn=record_expense, inputs=["text", "number"], outputs="text")
net_worth_ui = gr.Interface(fn=calculate_net_worth, inputs=None, outputs="text")
ledger_ui = gr.Interface(fn=get_ledger, inputs=None, outputs="json")

# 2. Group them into Tabs
app = gr.TabbedInterface(
    interface_list=[deposit_ui, exchange_ui, expense_ui, net_worth_ui, ledger_ui],
    tab_names=["Deposit", "Exchange", "Expense", "Net Worth", "Ledger"],
    title="NomadBank Multi-Currency Wallet"
)

# 3. Launch the app
if __name__ == "__main__":
    app.launch()