# calculator_tool.py
# This file contains the functions for our calculator tool.

def add(a, b):
    """Adds two numbers."""
    return float(a) + float(b)

def multiply(a, b):
    """Multiplies two numbers."""
    return float(a) * float(b)
    
def subtract(a, b):
    """Subtracts two numbers."""
    return float(a) - float(b)

def divide(a, b):
    """Divides two numbers, with a check for division by zero."""
    if float(b) == 0:
        return "Error: Division by zero is not allowed."
    return float(a) / float(b)
