import sqlite3
import uuid
from datetime import datetime
import json

DB = "creditguard.db"
CUSTOMER_ID = "CUST001"
CARD_ID = "CARD001"


def get_connection():
    return sqlite3.connect(DB)


def generate_id(prefix: str) -> str:
    return prefix + "-" + str(uuid.uuid4())[:8].upper()


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT,
                annual_income REAL,
                employment_status TEXT,
                credit_score INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credit_cards (
                card_id TEXT PRIMARY KEY,
                customer_id TEXT,
                current_limit REAL,
                current_balance REAL,
                status TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS card_transactions (
                transaction_id TEXT PRIMARY KEY,
                card_id TEXT,
                customer_id TEXT,
                datetime TEXT,
                merchant TEXT,
                description TEXT,
                amount REAL,
                category TEXT,
                suspicious_seed INTEGER DEFAULT 0,
                reviewed INTEGER DEFAULT 0,
                FOREIGN KEY(card_id) REFERENCES credit_cards(card_id),
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_history (
                payment_id TEXT PRIMARY KEY,
                card_id TEXT,
                customer_id TEXT,
                payment_date TEXT,
                amount REAL,
                status TEXT,
                days_late INTEGER DEFAULT 0,
                FOREIGN KEY(card_id) REFERENCES credit_cards(card_id),
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credit_limit_decisions (
                decision_id TEXT PRIMARY KEY,
                customer_id TEXT,
                old_limit REAL,
                new_limit REAL,
                decision TEXT,
                risk_score INTEGER,
                reasoning_summary TEXT,
                created_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor TEXT,
                datetime TEXT,
                type TEXT,
                message TEXT
            )
        """)

        conn.commit()


def reset_demo_data():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM audit_logs")
        cursor.execute("DELETE FROM credit_limit_decisions")
        cursor.execute("DELETE FROM card_transactions")
        cursor.execute("DELETE FROM credit_cards")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM payment_history")
        
        cursor.execute("""
            INSERT INTO customers (
                customer_id,
                name,
                annual_income,
                employment_status,
                credit_score
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            CUSTOMER_ID,
            "Sai",
            72000,
            "Full-time",
            735,
        ))

        cursor.execute("""
            INSERT INTO credit_cards (
                card_id,
                customer_id,
                current_limit,
                current_balance,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            CARD_ID,
            CUSTOMER_ID,
            3000,
            600,
            "Active",
        ))

        conn.commit()


def add_card_transaction(
    merchant: str,
    description: str,
    amount: float,
    category: str,
    suspicious_seed: int = 0,
):
    """
    Credit-card convention:
    - Purchase amount is positive and increases card balance.
    - Payment amount is negative and decreases card balance.
    """
    transaction_id = generate_id("TXN")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("BEGIN")

        cursor.execute("""
            INSERT INTO card_transactions (
                transaction_id,
                card_id,
                customer_id,
                datetime,
                merchant,
                description,
                amount,
                category,
                suspicious_seed,
                reviewed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_id,
            CARD_ID,
            CUSTOMER_ID,
            now,
            merchant,
            description,
            amount,
            category,
            suspicious_seed,
            0,
        ))

        cursor.execute("""
            UPDATE credit_cards
            SET current_balance = MAX(current_balance + ?, 0)
            WHERE card_id = ?
        """, (amount, CARD_ID))

        conn.commit()

    return transaction_id


def add_payment_history(
        amount: float,
        status: str,
        days_late: int = 0,
    ):
        payment_id = generate_id("PAY")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO payment_history (
                    payment_id,
                    card_id,
                    customer_id,
                    payment_date,
                    amount,
                    status,
                    days_late
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                payment_id,
                CARD_ID,
                CUSTOMER_ID,
                now,
                amount,
                status,
                days_late,
            ))

            conn.commit()

        return payment_id


def write_log(actor: str, log_type: str, message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (actor, datetime, type, message)
            VALUES (?, ?, ?, ?)
        """, (actor, now, log_type, message))
        conn.commit()
        
        
def save_credit_limit_decision(
    old_limit: float,
    new_limit: float,
    decision: str,
    risk_score: int,
    reasoning_summary: str,
):
    decision_id = generate_id("DEC")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO credit_limit_decisions (
                decision_id,
                customer_id,
                old_limit,
                new_limit,
                decision,
                risk_score,
                reasoning_summary,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            decision_id,
            CUSTOMER_ID,
            old_limit,
            new_limit,
            decision,
            risk_score,
            reasoning_summary,
            now,
        ))

        cursor.execute("""
            UPDATE credit_cards
            SET current_limit = ?
            WHERE card_id = ?
        """, (
            new_limit,
            CARD_ID,
        ))

        conn.commit()

    return decision_id