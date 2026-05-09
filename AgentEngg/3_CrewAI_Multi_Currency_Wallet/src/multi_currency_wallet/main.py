#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from multi_currency_wallet.crew import MultiCurrencyWalletCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements_str = """
A multi-currency digital wallet system (NomadBank). 
Users can hold balances in USD, EUR, GBP, and CAD.
Requirements:
1. Create/Manage account with multiple currency 'pockets'.
2. Deposit USD and Exchange funds between any supported currencies.
3. Record expenses in a specific currency.
4. Prevent spending more than the balance available in a specific pocket.
5. Calculate 'Total Net Worth' in USD using get_exchange_rate.
6. Provide a transaction ledger.
"""

module_name = "accounts.py"
class_name = "Account"


def run():
    """
    Run the engineering team crew.
    """
    inputs = {
        'requirements': requirements_str,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = MultiCurrencyWalletCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()