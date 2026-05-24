import gradio as gr
import pandas as pd
import plotly.express as px

from database import (
    get_connection,
    init_db,
    reset_demo_data,
)

from transactionSimulator import (
    add_regular_card_transaction,
    add_risky_card_transaction,
    add_card_payment,
    add_on_time_payment_record,
    add_late_payment_record,
)

from creditAnalystSimulator import run_fake_credit_analyst
from credit_analyst_agent import run_credit_analyst_agent

class CreditDashboardView:
    """
    This mirrors the TraderView idea from the trading simulator.
    It reads state from SQLite and returns Gradio-ready values.
    """

    def get_card_summary_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    c.customer_id,
                    c.name,
                    c.annual_income,
                    c.employment_status,
                    c.credit_score,
                    cc.card_id,
                    ROUND(cc.current_limit, 2) AS current_limit,
                    ROUND(cc.current_balance, 2) AS current_balance,
                    ROUND((cc.current_balance / cc.current_limit) * 100, 2) AS utilization_percent,
                    cc.status
                FROM customers c
                JOIN credit_cards cc ON c.customer_id = cc.customer_id
            """, conn)

    def get_transactions_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    transaction_id,
                    datetime,
                    merchant,
                    description,
                    ROUND(amount, 2) AS amount,
                    category,
                    suspicious_seed,
                    reviewed
                FROM card_transactions
                ORDER BY datetime DESC
                LIMIT 20
            """, conn)

    def get_decisions_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    decision_id,
                    created_at,
                    decision,
                    old_limit,
                    new_limit,
                    risk_score,
                    reasoning_summary
                FROM credit_limit_decisions
                ORDER BY created_at DESC
                LIMIT 10
            """, conn)

    def get_logs_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    datetime,
                    actor,
                    type,
                    message
                FROM audit_logs
                ORDER BY id DESC
                LIMIT 20
            """, conn)

    def get_utilization_chart(self):
        df = self.get_card_summary_df()

        if df.empty:
            return px.bar(title="Credit Card Utilization")

        fig = px.bar(
            df,
            x="card_id",
            y="utilization_percent",
            title="Credit Card Utilization",
            text="utilization_percent",
        )

        fig.update_layout(
            yaxis_title="Utilization %",
            xaxis_title="Card",
        )

        return fig

    def get_summary_html(self):
        df = self.get_card_summary_df()

        if df.empty:
            return "<div>No card data found.</div>"

        row = df.iloc[0]

        return f"""
        <div style='padding:16px; border-radius:12px; background:#f3f4f6;'>
            <h2>CreditGuard Summary</h2>
            <p><b>Customer:</b> {row['name']} | <b>Credit Score:</b> {row['credit_score']}</p>
            <p><b>Annual Income:</b> ${row['annual_income']:,.2f}</p>
            <p><b>Employment:</b> {row['employment_status']}</p>
            <p><b>Current Limit:</b> ${row['current_limit']:,.2f}</p>
            <p><b>Current Balance:</b> ${row['current_balance']:,.2f}</p>
            <p><b>Utilization:</b> {row['utilization_percent']:.2f}%</p>
        </div>
        """

    def get_latest_decision_html(self):
        with get_connection() as conn:
            df = pd.read_sql_query("""
                SELECT
                    decision,
                    old_limit,
                    new_limit,
                    risk_score,
                    reasoning_summary,
                    created_at
                FROM credit_limit_decisions
                ORDER BY created_at DESC
                LIMIT 1
            """, conn)

        if df.empty:
            return """
            <div style='padding:16px; border-radius:12px; background:#fff7ed;'>
                <h2>Latest Credit Analyst Decision</h2>
                <p>No credit limit decision has been made yet.</p>
                <p>Click <b>Run Credit Analyst Simulator</b> to generate a decision.</p>
            </div>
            """

        row = df.iloc[0]

        decision = row["decision"]
        old_limit = row["old_limit"]
        new_limit = row["new_limit"]
        risk_score = row["risk_score"]
        reasoning = row["reasoning_summary"]
        created_at = row["created_at"]

        return f"""
        <div style='padding:16px; border-radius:12px; background:#ecfdf5;'>
            <h2>Latest Credit Analyst Decision</h2>
            <p><b>Decision:</b> {decision}</p>
            <p><b>Old Limit:</b> ${old_limit:,.2f}</p>
            <p><b>New Limit:</b> ${new_limit:,.2f}</p>
            <p><b>Risk Score:</b> {risk_score}/100</p>
            <p><b>Reasoning:</b> {reasoning}</p>
            <p><b>Created At:</b> {created_at}</p>
        </div>
        """
        
    def get_evidence_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    c.credit_score,
                    c.annual_income,
                    cc.current_limit,
                    cc.current_balance,
                    ROUND((cc.current_balance / cc.current_limit) * 100, 2) AS utilization_percent,
                    (
                        SELECT COUNT(*)
                        FROM card_transactions
                        WHERE suspicious_seed = 1
                    ) AS risky_transaction_count,
                    (
                        SELECT COUNT(*)
                        FROM card_transactions
                    ) AS total_transaction_count,
                    (
                        SELECT COUNT(*)
                        FROM payment_history
                        WHERE status = 'Late'
                    ) AS late_payment_count,
                    (
                        SELECT COUNT(*)
                        FROM payment_history
                        WHERE status = 'On Time'
                    ) AS on_time_payment_count
                FROM customers c
                JOIN credit_cards cc ON c.customer_id = cc.customer_id
                LIMIT 1
            """, conn)
            
    def get_payment_history_df(self):
        with get_connection() as conn:
            return pd.read_sql_query("""
                SELECT
                    payment_id,
                    payment_date,
                    amount,
                    status,
                    days_late
                FROM payment_history
                ORDER BY payment_date DESC
                LIMIT 20
            """, conn)
        

    def refresh(self, status_message="Dashboard refreshed."):
        """
        IMPORTANT:
        The return order must match the Gradio outputs list exactly.
        """
        return (
            status_message,
            self.get_summary_html(),
            self.get_latest_decision_html(),
            self.get_card_summary_df(),
            self.get_transactions_df(),
            self.get_decisions_df(),
            self.get_logs_df(),
            self.get_utilization_chart(),
            self.get_evidence_df(),
            self.get_payment_history_df(),
        )


view = CreditDashboardView()


def add_regular_and_refresh():
    message = add_regular_card_transaction()
    return view.refresh(message)


def add_risky_and_refresh():
    message = add_risky_card_transaction()
    return view.refresh(message)


def add_payment_and_refresh():
    message = add_card_payment()
    return view.refresh(message)


def reset_and_refresh():
    reset_demo_data()
    return view.refresh("Demo data reset successfully.")


def run_credit_analyst_and_refresh():
    message = run_fake_credit_analyst()
    return view.refresh(message)


def add_on_time_payment_and_refresh():
    message = add_on_time_payment_record()
    return view.refresh(message)


def add_late_payment_and_refresh():
    message = add_late_payment_record()
    return view.refresh(message)


def run_real_credit_analyst_and_refresh():
    message = run_credit_analyst_agent()
    return view.refresh(message)


def create_ui():
    init_db()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]

    if count == 0:
        reset_demo_data()

    with gr.Blocks(title="CreditGuard Dashboard", fill_width=True) as ui:
        gr.Markdown("# CreditGuard MCP — Basic Dashboard")
        gr.Markdown(
            "Small starter: simulated credit-card transactions + dashboard. "
            "Agent and MCP come next."
        )

        status = gr.Textbox(label="Status", lines=6)

        with gr.Row():
            summary = gr.HTML()
            latest_decision = gr.HTML()

        with gr.Row():
            regular_btn = gr.Button("Add Regular Card Transaction")
            risky_btn = gr.Button("Add Risky Card Transaction")
            payment_btn = gr.Button("Add Card Payment")
            on_time_payment_btn = gr.Button("Add On-Time Payment")
            late_payment_btn = gr.Button("Add Late Payment")

        with gr.Row():
            run_analyst_btn = gr.Button(
                "Run Credit Analyst Simulator",
                variant="primary",
            )
            reset_btn = gr.Button("Reset Demo Data", variant="stop")
            run_real_agent_btn = gr.Button(
                "Run Credit Analyst Agent",
                variant="primary",
                    )

        card_summary = gr.Dataframe(label="Card Summary")
        transactions = gr.Dataframe(label="Recent Card Transactions")
        payment_history = gr.Dataframe(label="Payment History")
        utilization_chart = gr.Plot(label="Utilization Chart")
        evidence = gr.Dataframe(label="Credit Analyst Evidence")

        decisions = gr.Dataframe(label="Credit Limit Decisions")
        logs = gr.Dataframe(label="Agent/Audit Logs")

        outputs = [
            status,
            summary,
            latest_decision,
            card_summary,
            transactions,
            decisions,
            logs,
            utilization_chart,
            evidence,
            payment_history,
        ]

        regular_btn.click(
            fn=add_regular_and_refresh,
            outputs=outputs,
        )

        risky_btn.click(
            fn=add_risky_and_refresh,
            outputs=outputs,
        )

        payment_btn.click(
            fn=add_payment_and_refresh,
            outputs=outputs,
        )

        run_analyst_btn.click(
            fn=run_credit_analyst_and_refresh,
            outputs=outputs,
        )

        reset_btn.click(
            fn=reset_and_refresh,
            outputs=outputs,
        )
        
        on_time_payment_btn.click(
            fn=add_on_time_payment_and_refresh,
            outputs=outputs,
        )

        late_payment_btn.click(
            fn=add_late_payment_and_refresh,
            outputs=outputs,
        )
        
        run_real_agent_btn.click(
            fn=run_real_credit_analyst_and_refresh,
            outputs=outputs,
        )

        ui.load(
            fn=view.refresh,
            outputs=outputs,
        )

    return ui


if __name__ == "__main__":
    app = create_ui()
    app.launch(inbrowser=True)