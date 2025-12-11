#==========Class version================

import csv      #csv module to read and write csv files 
import os       #os module to interact with the operating system
import json     #json module to read and write json files
import sys
from datetime import datetime       #datetime module to work with date and time
from typing import List, Dict, Optional     #typing module to define types
from dataclasses import dataclass, asdict       
from collections import defaultdict

@dataclass
class Expense:
    id: int
    description: str
    amount: float
    category: str
    date: str 

class ExpenseTracker:
    def __init__(self, expense_file='expense.json', budget_file='budgets.json'):
        self.expense_file = expense_file
        self.budget_file = budget_file
        self.expenses = self.load_expenses()
        self.budgets = self.load_budgets()
        self.next_id = max([expense.id for expense in self.expenses], default=0) + 1

    
    def load_expenses(self) -> List[Expense]:
        if os.path.exists(self.expense_file):
            try:
                with open(self.expense_file, 'r') as f:
                    data = json.load(f)
                    return [Expense(**item) for item in data]
            except (FileNotFoundError, json.JSONDecodeError):
                return []
        return []

    def load_budgets(self) -> Dict[str, float]:
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}
        return {}

    def save_expenses(self):
        with open(self.expense_file, 'w') as f:
            json.dump([asdict(expense) for expense in self.expenses], f, indent=2)
        
    def save_budgets(self):
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f, indent=2)
    
    def add_expense(self, description: str, amount:float, category: str = "other"):
        """Add a new expense"""
        if amount <= 0:
            print("Error: Amount must be positive.")
            return 
        
        expense = Expense(
            id=self.next_id,
            description=description,
            amount=amount,
            category=category,
            date=datetime.now().strftime('%Y-%m-%d')
        )

        self.expenses.append(expense)
        self.next_id += 1
        self.save_expenses()

        self.check_budget(expense.date[:7])

        print(f"Expense added successfully! (ID: {expense.id})")
        print(f"Description: {expense.description}, Amount: {expense.amount}, Category: {expense.category}, Date: {expense.date}")

    
    def update_expense(self, expense_id:int, **kwargs):
        for expense in self.expenses:
            if expense_id == expense.id:
                for key, value in kwargs.items():
                    if hasattr(expense, key):
                        setattr(expense, key, value)
                self.save_expenses()
                print(f"Expense updated successfully! (ID: {expense_id})")
                return

        print(f"Error: Expense with ID {expense_id} not found.")

    def delete_expenses(self, expense_id:int):
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                self.expenses.pop(i)
                self.save_expenses()
                print(f"Expense deleted successfully! (ID: {expense_id})")
                return

        print(f"Error: Expense with ID {expense_id} not found.")

    def view_all_expenses(self, filter_category: Optional[str] = None):
        if not self.expenses:
            print("No expenses found.")
            return
        
        filtered_expenses = self.expenses
        if filter_category:
            filtered_expenses = [e for e in self.expenses if e.category.lower() == filter_category.lower()]
            if not filtered_expenses:
                print(f"No expenses found for category: {filter_category}")
                return
            
        print("\n" + "=" * 60)
        print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Description':<25} {'Amount':<10}")
        print("-"*60)

    

    def check_budget(self):
        pass

