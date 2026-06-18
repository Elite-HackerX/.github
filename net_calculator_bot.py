"""
Net Calculator Bot
A Discord/Slack bot for calculating net income, net worth, and financial metrics.
"""

import os
from decimal import Decimal
from typing import Dict, List, Tuple

class NetCalculatorBot:
    """Bot for performing financial net calculations."""
    
    def __init__(self):
        self.transactions: List[Dict] = []
        self.assets: Dict[str, Decimal] = {}
        self.liabilities: Dict[str, Decimal] = {}
    
    def calculate_net_income(self, gross_income: float, deductions: Dict[str, float]) -> float:
        """
        Calculate net income from gross income minus deductions.
        
        Args:
            gross_income: Total earned income before deductions
            deductions: Dictionary of deduction categories and amounts
                       e.g., {"taxes": 5000, "insurance": 1000}
        
        Returns:
            Net income after all deductions
        """
        total_deductions = sum(deductions.values())
        net_income = gross_income - total_deductions
        
        return max(0, net_income)
    
    def calculate_net_worth(self, assets: Dict[str, float], liabilities: Dict[str, float]) -> Dict:
        """
        Calculate net worth (assets - liabilities).
        
        Args:
            assets: Dictionary of asset categories and values
                   e.g., {"cash": 10000, "investments": 50000, "property": 200000}
            liabilities: Dictionary of liability categories and amounts
                        e.g., {"mortgage": 150000, "car_loan": 25000}
        
        Returns:
            Dictionary containing total assets, liabilities, and net worth
        """
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        net_worth = total_assets - total_liabilities
        
        return {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "net_worth": net_worth,
            "assets_breakdown": assets,
            "liabilities_breakdown": liabilities
        }
    
    def calculate_net_profit(self, revenue: float, expenses: Dict[str, float]) -> Dict:
        """
        Calculate net profit from revenue minus expenses.
        
        Args:
            revenue: Total income from sales or services
            expenses: Dictionary of expense categories
                     e.g., {"salaries": 50000, "rent": 12000, "supplies": 5000}
        
        Returns:
            Dictionary with revenue, expenses, and net profit
        """
        total_expenses = sum(expenses.values())
        net_profit = revenue - total_expenses
        profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
        
        return {
            "revenue": revenue,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "profit_margin_percent": round(profit_margin, 2),
            "expense_breakdown": expenses
        }
    
    def calculate_net_savings(self, income: float, expenses: float, investments: float = 0) -> Dict:
        """
        Calculate net savings rate and amount.
        
        Args:
            income: Total monthly/yearly income
            expenses: Total monthly/yearly expenses
            investments: Optional investment amount
        
        Returns:
            Dictionary with savings metrics
        """
        net_savings = income - expenses - investments
        savings_rate = (net_savings / income * 100) if income > 0 else 0
        
        return {
            "income": income,
            "expenses": expenses,
            "investments": investments,
            "net_savings": net_savings,
            "savings_rate_percent": round(savings_rate, 2)
        }
    
    def add_transaction(self, description: str, amount: float, category: str, transaction_type: str):
        """Add a transaction to the history."""
        self.transactions.append({
            "description": description,
            "amount": amount,
            "category": category,
            "type": transaction_type  # 'income' or 'expense'
        })
    
    def get_net_by_category(self) -> Dict[str, float]:
        """Calculate net amount by category."""
        category_net = {}
        
        for transaction in self.transactions:
            category = transaction["category"]
            amount = transaction["amount"]
            multiplier = 1 if transaction["type"] == "income" else -1
            
            if category not in category_net:
                category_net[category] = 0
            
            category_net[category] += amount * multiplier
        
        return category_net
    
    def format_currency(self, amount: float, currency: str = "$") -> str:
        """Format amount as currency string."""
        return f"{currency}{amount:,.2f}"
    
    def generate_net_report(self) -> str:
        """Generate a formatted net calculation report."""
        category_net = self.get_net_by_category()
        total_net = sum(category_net.values())
        
        report = "=== NET CALCULATION REPORT ===\n\n"
        
        for category, net_amount in sorted(category_net.items()):
            status = "+" if net_amount >= 0 else ""
            report += f"{category}: {status}{self.format_currency(net_amount)}\n"
        
        report += f"\n{'─' * 35}\n"
        status = "+" if total_net >= 0 else ""
        report += f"TOTAL NET: {status}{self.format_currency(total_net)}\n"
        
        return report


# Example usage and commands for bot integration
def bot_commands():
    """Example commands for Discord/Slack integration."""
    
    calculator = NetCalculatorBot()
    
    # Example 1: Net Income Calculation
    print("=" * 50)
    print("EXAMPLE 1: NET INCOME CALCULATION")
    print("=" * 50)
    gross = 5000
    deductions = {"taxes": 800, "insurance": 200, "retirement": 300}
    net_income = calculator.calculate_net_income(gross, deductions)
    print(f"Gross Income: {calculator.format_currency(gross)}")
    print(f"Deductions: {deductions}")
    print(f"Net Income: {calculator.format_currency(net_income)}\n")
    
    # Example 2: Net Worth Calculation
    print("=" * 50)
    print("EXAMPLE 2: NET WORTH CALCULATION")
    print("=" * 50)
    assets = {"cash": 10000, "investments": 50000, "property": 200000}
    liabilities = {"mortgage": 150000, "car_loan": 25000, "credit_card": 5000}
    net_worth_report = calculator.calculate_net_worth(assets, liabilities)
    print(f"Assets: {calculator.format_currency(net_worth_report['total_assets'])}")
    print(f"Liabilities: {calculator.format_currency(net_worth_report['total_liabilities'])}")
    print(f"Net Worth: {calculator.format_currency(net_worth_report['net_worth'])}\n")
    
    # Example 3: Net Profit Calculation
    print("=" * 50)
    print("EXAMPLE 3: NET PROFIT CALCULATION")
    print("=" * 50)
    revenue = 100000
    expenses = {"salaries": 50000, "rent": 10000, "supplies": 5000, "utilities": 2000}
    profit_report = calculator.calculate_net_profit(revenue, expenses)
    print(f"Revenue: {calculator.format_currency(profit_report['revenue'])}")
    print(f"Expenses: {calculator.format_currency(profit_report['total_expenses'])}")
    print(f"Net Profit: {calculator.format_currency(profit_report['net_profit'])}")
    print(f"Profit Margin: {profit_report['profit_margin_percent']}%\n")
    
    # Example 4: Net Savings Calculation
    print("=" * 50)
    print("EXAMPLE 4: NET SAVINGS CALCULATION")
    print("=" * 50)
    savings_report = calculator.calculate_net_savings(income=5000, expenses=3500, investments=500)
    print(f"Income: {calculator.format_currency(savings_report['income'])}")
    print(f"Expenses: {calculator.format_currency(savings_report['expenses'])}")
    print(f"Investments: {calculator.format_currency(savings_report['investments'])}")
    print(f"Net Savings: {calculator.format_currency(savings_report['net_savings'])}")
    print(f"Savings Rate: {savings_report['savings_rate_percent']}%\n")


if __name__ == "__main__":
    bot_commands()
