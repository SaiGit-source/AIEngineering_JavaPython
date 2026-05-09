from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ExchangeRateInput(BaseModel):
    """Input schema for ExchangeRateTool."""
    base_currency: str = Field(..., description="The currency to convert from (e.g., USD, EUR, GBP, CAD).")
    target_currency: str = Field(..., description="The currency to convert to (e.g., USD, EUR, GBP, CAD).")

class ExchangeRateTool(BaseTool):
    name: str = "get_exchange_rate"
    description: str = (
        "Lookup the current conversion rate between USD, EUR, GBP, and CAD. "
        "Use this for currency exchanges or calculating total portfolio value."
    )
    args_schema: Type[BaseModel] = ExchangeRateInput

    def _run(self, base_currency: str, target_currency: str) -> float:
        rates = {
            "USD_EUR": 0.92, "USD_GBP": 0.79, "USD_CAD": 1.36,
            "EUR_USD": 1.08, "EUR_GBP": 0.85, "EUR_CAD": 1.48,
            "GBP_USD": 1.26, "GBP_EUR": 1.17, "GBP_CAD": 1.73,
            "CAD_USD": 0.73, "CAD_EUR": 0.67, "CAD_GBP": 0.58
        }
        
        base = base_currency.upper()
        target = target_currency.upper()
        
        if base == target:
            return 1.0
            
        pair = f"{base}_{target}"
        return rates.get(pair, 1.0)
