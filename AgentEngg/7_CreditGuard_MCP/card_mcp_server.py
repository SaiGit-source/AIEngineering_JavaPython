import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from database import (
    get_connection,
    CUSTOMER_ID,
    CARD_ID,
    generate_id,
)

mcp = FastMCP("CreditGuard Card MCP Server")


@mcp.tool()
def get_credit_profile() -> str:
    """
    Return customer credit profile, card limit, balance, utilization,
    risky transaction count, and late payment count.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customer_id,
                c.name,
                c.annual_income,
                c.employment_status,
                c.credit_score,
                cc.card_id,
                cc.current_limit,
                cc.current_balance,
                ROUND((cc.current_balance / cc.current_limit) * 100, 2) AS utilization_percent,
                cc.status
            FROM customers c
            JOIN credit_cards cc ON c.customer_id = cc.customer_id
            WHERE c.customer_id = ?
        """, (CUSTOMER_ID,))

        row = cursor.fetchone()

        if not row:
            return json.dumps({"error": "Customer profile not found"})

        cursor.execute("""
            SELECT COUNT(*)
            FROM card_transactions
            WHERE suspicious_seed = 1
        """)
        risky_transaction_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM payment_history
            WHERE status = 'Late'
        """)
        late_payment_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM payment_history
            WHERE status = 'On Time'
        """)
        on_time_payment_count = cursor.fetchone()[0]

    return json.dumps({
        "customer_id": row[0],
        "name": row[1],
        "annual_income": row[2],
        "employment_status": row[3],
        "credit_score": row[4],
        "card_id": row[5],
        "current_limit": row[6],
        "current_balance": row[7],
        "utilization_percent": row[8],
        "card_status": row[9],
        "risky_transaction_count": risky_transaction_count,
        "late_payment_count": late_payment_count,
        "on_time_payment_count": on_time_payment_count,
    })


@mcp.tool()
def get_recent_transactions(limit: int = 10) -> str:
    """
    Return recent credit-card transactions.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                transaction_id,
                datetime,
                merchant,
                description,
                amount,
                category,
                suspicious_seed,
                reviewed
            FROM card_transactions
            ORDER BY datetime DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

    transactions = [
        {
            "transaction_id": row[0],
            "datetime": row[1],
            "merchant": row[2],
            "description": row[3],
            "amount": row[4],
            "category": row[5],
            "suspicious_seed": row[6],
            "reviewed": row[7],
        }
        for row in rows
    ]

    return json.dumps(transactions)


@mcp.tool()
def get_payment_history(limit: int = 10) -> str:
    """
    Return recent payment history.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                payment_id,
                payment_date,
                amount,
                status,
                days_late
            FROM payment_history
            ORDER BY payment_date DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

    payments = [
        {
            "payment_id": row[0],
            "payment_date": row[1],
            "amount": row[2],
            "status": row[3],
            "days_late": row[4],
        }
        for row in rows
    ]

    return json.dumps(payments)


@mcp.tool()
def save_credit_decision(
    decision: str,
    old_limit: float,
    new_limit: float,
    risk_score: int,
    reasoning_summary: str,
) -> str:
    """
    Save the credit analyst decision and update the simulated card limit.
    Decision should be one of: Increase, Decrease, No Change, Manual Review.
    """
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

    return json.dumps({
        "decision_id": decision_id,
        "decision": decision,
        "old_limit": old_limit,
        "new_limit": new_limit,
        "risk_score": risk_score,
        "reasoning_summary": reasoning_summary,
        "created_at": now,
    })


@mcp.tool()
def write_audit_log(actor: str, log_type: str, message: str) -> str:
    """
    Write an audit log entry.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO audit_logs (
                actor,
                datetime,
                type,
                message
            )
            VALUES (?, ?, ?, ?)
        """, (
            actor,
            now,
            log_type,
            message,
        ))

        conn.commit()

    return json.dumps({
        "status": "saved",
        "actor": actor,
        "type": log_type,
        "message": message,
        "datetime": now,
    })


if __name__ == "__main__":
    mcp.run()