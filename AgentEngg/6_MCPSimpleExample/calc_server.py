from mcp.server.fastmcp import FastMCP
from calculator import Calculator

# 1. Initialize the MCP Server
mcp = FastMCP("calc_server")

# 2. Instantiate the Calculator object instance to provide the required 'self' context
calc = Calculator(num1=0.0, num2=0.0)

@mcp.tool()
async def get_current_dateTime() -> str:
    """Get the current date and time.

    Returns:
        The current date and time as an ISO string.
    """
    # Fix: Route through the 'calc' instance object
    return calc.get_current_datetime().format()

@mcp.tool()
async def add(num1: float, num2: float) -> float:
    """Add two numbers.

    Args:
        num1: The first number
        num2: The second number

    Returns:
        The sum of the two numbers
    """
    # Fix: Route through the 'calc' instance object
    return calc.add(num1, num2)

@mcp.tool()
async def subtract(num1: float, num2: float) -> float:
    """Subtract two numbers.

    Args:
        num1: The first number
        num2: The second number

    Returns:
        The difference of the two numbers
    """
    # Fix: Route through the 'calc' instance object
    return calc.subtract(num1, num2)

@mcp.tool()
async def multiply(num1: float, num2: float) -> float:
    """Multiply two numbers.

    Args:
        num1: The first number
        num2: The second number

    Returns:
        The product of the two numbers
    """
    # Fix: Route through the 'calc' instance object
    return calc.multiply(num1, num2)

# 4. Start the server transport layer safely
if __name__ == "__main__":
    mcp.run(transport="stdio")
