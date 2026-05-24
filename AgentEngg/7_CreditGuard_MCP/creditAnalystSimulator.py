from database import (
    get_connection,
    save_credit_limit_decision,
    write_log,
    CUSTOMER_ID,
)


def get_credit_profile():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.credit_score,
                c.annual_income,
                cc.current_limit,
                cc.current_balance,
                ROUND((cc.current_balance / cc.current_limit) * 100, 2) AS utilization_percent
            FROM customers c
            JOIN credit_cards cc ON c.customer_id = cc.customer_id
            WHERE c.customer_id = ?
        """, (CUSTOMER_ID,))

        row = cursor.fetchone()

    if not row:
        raise ValueError("Customer credit profile not found.")

    return {
        "credit_score": row[0],
        "annual_income": row[1],
        "current_limit": row[2],
        "current_balance": row[3],
        "utilization_percent": row[4],
    }


def count_risky_transactions():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM card_transactions
            WHERE suspicious_seed = 1
        """)

        return cursor.fetchone()[0]


def run_fake_credit_analyst():
    """
    This is a temporary fake Credit Analyst.
    Later, we will replace this with the real OpenAI Agent + MCP version.
    """
    profile = get_credit_profile()
    risky_count = count_risky_transactions()
    late_payment_count = count_late_payments()

    credit_score = profile["credit_score"]
    annual_income = profile["annual_income"]
    old_limit = profile["current_limit"]
    utilization = profile["utilization_percent"]

    write_log("CreditAnalystSimulator", "start", "Started credit limit review")

    risk_score = 0
    risk_factors = []

    # Credit score risk
    if credit_score < 620:
        risk_score += 35
        risk_factors.append("credit score is below 620")
    elif credit_score < 680:
        risk_score += 20
        risk_factors.append("credit score is below 680")
    elif credit_score < 720:
        risk_score += 10
        risk_factors.append("credit score is slightly below preferred range")

    # Utilization risk
    if utilization > 90:
        risk_score += 35
        risk_factors.append("credit utilization is above 90%")
    elif utilization > 75:
        risk_score += 25
        risk_factors.append("credit utilization is above 75%")
    elif utilization > 50:
        risk_score += 10
        risk_factors.append("credit utilization is above 50%")

    # Income risk
    if annual_income < 40000:
        risk_score += 20
        risk_factors.append("annual income is below $40,000")
    elif annual_income < 60000:
        risk_score += 10
        risk_factors.append("annual income is below $60,000")

    # Risky transaction risk
    if risky_count > 0:
        risky_points = risky_count * 10
        risk_score += risky_points
        risk_factors.append(f"{risky_count} risky transaction(s) found")

    # Late payment risk
    if late_payment_count > 0:
        late_payment_points = late_payment_count * 20
        risk_score += late_payment_points
        risk_factors.append(f"{late_payment_count} late payment(s) found")

        write_log(
            "CreditAnalystSimulator",
            "risk",
            f"Found {late_payment_count} late payment(s).",
        )

    risk_score = min(risk_score, 100)

    # Decision logic
    if (
        risk_score <= 25
        and utilization < 40
        and credit_score >= 700
        and late_payment_count == 0
    ):
        decision = "Increase"
        new_limit = old_limit * 1.5
        reasoning = (
            "Customer qualifies for a credit limit increase because credit score is strong, "
            "utilization is low, income is stable, there are no late payments, and risky "
            "transaction count is low."
        )

    elif risk_score >= 75 or utilization > 90 or late_payment_count >= 2:
        decision = "Decrease"
        new_limit = max(old_limit * 0.75, 1000)
        reasoning = (
            "Credit limit decrease recommended because the customer shows high risk indicators, "
            "such as high utilization, late payment history, and/or multiple risky transactions."
        )

    elif risk_score >= 45 or late_payment_count == 1:
        decision = "Manual Review"
        new_limit = old_limit
        reasoning = (
            "Manual review recommended because the customer has moderate risk indicators. "
            "A human credit analyst should review the account before changing the limit."
        )

    else:
        decision = "No Change"
        new_limit = old_limit
        reasoning = (
            "No credit limit change recommended. Customer profile is acceptable, "
            "but does not strongly qualify for an increase."
        )

    if risk_factors:
        reasoning += " Main risk factors: " + ", ".join(risk_factors) + "."
    else:
        reasoning += " No major risk factors were found."

    decision_id = save_credit_limit_decision(
        old_limit=old_limit,
        new_limit=new_limit,
        decision=decision,
        risk_score=risk_score,
        reasoning_summary=reasoning,
    )

    write_log(
        "CreditAnalystSimulator",
        "decision",
        f"{decision} decision saved as {decision_id}. Risk score: {risk_score}",
    )

    return (
        f"Credit Analyst Review Complete\n\n"
        f"Decision: {decision}\n"
        f"Old Limit: ${old_limit:,.2f}\n"
        f"New Limit: ${new_limit:,.2f}\n"
        f"Risk Score: {risk_score}/100\n"
        f"Risky Transactions: {risky_count}\n"
        f"Late Payments: {late_payment_count}\n\n"
        f"Reasoning: {reasoning}"
    )
    
    
def count_late_payments():
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM payment_history
                WHERE status = 'Late'
            """)

            return cursor.fetchone()[0]