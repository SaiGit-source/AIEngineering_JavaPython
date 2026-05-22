from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime


class Calculator(BaseModel):
    num1: float = 0.0
    num2: float = 0.0


    def add(self, num1: float, num2: float) -> float:
        return num1 + num2
    
    def subtract(self, num1: float, num2: float) -> float:
        return num1 - num2
    
    def multiply(self, num1: float, num2: float) -> float:
        return num1 * num2
    
    def divide(self, num1: float, num2: float) -> float:
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    
    def get_current_datetime(self):
        return datetime.now().isoformat()
