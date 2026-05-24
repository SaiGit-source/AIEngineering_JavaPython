import random
from database import add_card_transaction, add_payment_history


regular_card_transactions = [
    {
        "merchant": "Tim Hortons",
        "description": "Coffee purchase",
        "amount": 4.75,
        "category": "Food",
    },
    {
        "merchant": "Walmart",
        "description": "Groceries",
        "amount": 86.20,
        "category": "Groceries",
    },
    {
        "merchant": "Netflix",
        "description": "Monthly subscription",
        "amount": 18.99,
        "category": "Entertainment",
    },
    {
        "merchant": "TTC",
        "description": "Transit fare",
        "amount": 3.35,
        "category": "Transportation",
    },
]


risky_card_transactions = [
    {
        "merchant": "Unknown Crypto Exchange",
        "description": "Crypto-related purchase",
        "amount": 950.00,
        "category": "Unknown",
    },
    {
        "merchant": "Luxury Electronics Store",
        "description": "High-value electronics purchase",
        "amount": 1200.00,
        "category": "Shopping",
    },
    {
        "merchant": "Foreign Gambling Site",
        "description": "International gambling transaction",
        "amount": 700.00,
        "category": "Gambling",
    },
    {
        "merchant": "Cash Advance ATM",
        "description": "Cash advance withdrawal",
        "amount": 500.00,
        "category": "Cash Advance",
    },
]


def add_regular_card_transaction():
    txn = random.choice(regular_card_transactions)

    transaction_id = add_card_transaction(
        merchant=txn["merchant"],
        description=txn["description"],
        amount=txn["amount"],
        category=txn["category"],
        suspicious_seed=0,
    )

    return (
        f"Added regular card transaction: "
        f"{transaction_id} | {txn['merchant']} | ${txn['amount']:,.2f}"
    )


def add_risky_card_transaction():
    txn = random.choice(risky_card_transactions)

    transaction_id = add_card_transaction(
        merchant=txn["merchant"],
        description=txn["description"],
        amount=txn["amount"],
        category=txn["category"],
        suspicious_seed=1,
    )

    return (
        f"Added risky card transaction: "
        f"{transaction_id} | {txn['merchant']} | ${txn['amount']:,.2f}"
    )


def add_card_payment():
    transaction_id = add_card_transaction(
        merchant="Customer Payment",
        description="Credit card payment",
        amount=-300.00,
        category="Payment",
        suspicious_seed=0,
    )

    return f"Added card payment: {transaction_id} | -$300.00"


def add_on_time_payment_record():
    payment_id = add_payment_history(
        amount=300.00,
        status="On Time",
        days_late=0,
    )

    return f"Added on-time payment record: {payment_id} | $300.00"


def add_late_payment_record():
    payment_id = add_payment_history(
        amount=150.00,
        status="Late",
        days_late=18,
    )

    return f"Added late payment record: {payment_id} | $150.00 | 18 days late"