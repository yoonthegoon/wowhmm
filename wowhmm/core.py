from typing import List, NamedTuple, Dict


class SimpleTable:
    """A simple table implementation to replace pandas DataFrame functionality."""
    
    def __init__(self, data: Dict[str, Dict[str, float]], index: List[str], columns: List[str]):
        self.data = data
        self.index = index
        self.columns = columns
    
    def __str__(self):
        """String representation that mimics pandas DataFrame output."""
        # Calculate column widths
        col_widths = {}
        
        # Start with column names
        for col in self.columns:
            col_widths[col] = len(col)
        
        # Check data values
        for row in self.index:
            for col in self.columns:
                value_str = f"{self.data[row][col]:.2f}"
                col_widths[col] = max(col_widths[col], len(value_str))
        
        # Check row names
        max_index_width = max(len(name) for name in self.index)
        
        # Build the string
        lines = []
        
        # Header line
        header = " " * max_index_width
        for col in self.columns:
            header += f"  {col:>{col_widths[col]}}"
        lines.append(header)
        
        # Data lines
        for row in self.index:
            line = f"{row:<{max_index_width}}"
            for col in self.columns:
                value_str = f"{self.data[row][col]:.2f}"
                line += f"  {value_str:>{col_widths[col]}}"
            lines.append(line)
        
        return "\n".join(lines)
    
    def __repr__(self):
        return self.__str__()


class Spend(NamedTuple):
    """
    Who spent amount for whom.

    :param who: The person who spent the money
    :param amount: The amount of money spent
    :param for_whom: The people for whom the money was spent
    """

    who: str
    amount: float
    for_whom: List[str]


class Ledger:
    def __init__(self, transactions: List[Spend] = None):
        """
        A ledger of transactions.

        :param transactions: A list of transactions
        """

        self.transactions = transactions or []
        if not all(isinstance(transaction, Spend) for transaction in self.transactions):
            self.transactions = [
                Spend(who, amount, for_whom) for who, amount, for_whom in transactions
            ]

    def tabulate(self) -> SimpleTable:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: A SimpleTable of who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        # Initialize data dictionary
        data = {}
        for name in names:
            data[name] = {other_name: 0.0 for other_name in names}

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    data[payer][payee] -= value
                    data[payee][payer] += value

        return SimpleTable(data, names, names)
