from typing import Dict, List, NamedTuple


class LedgerMatrix:
    """
    A simple matrix-like structure to replace pandas DataFrame for our specific use case.
    """
    
    def __init__(self, names: List[str]):
        self.names = sorted(names)
        self.data = {name: {other: 0.0 for other in self.names} for name in self.names}
    
    def set_value(self, row: str, col: str, value: float):
        """Set a value in the matrix."""
        self.data[row][col] = value
    
    def get_value(self, row: str, col: str) -> float:
        """Get a value from the matrix."""
        return self.data[row][col]
    
    def add_to_value(self, row: str, col: str, value: float):
        """Add a value to an existing value in the matrix."""
        self.data[row][col] += value
    
    def __str__(self) -> str:
        """String representation of the matrix similar to pandas DataFrame."""
        # Calculate column widths for alignment
        col_widths = {}
        for name in self.names:
            max_width = len(name)
            for other in self.names:
                value_str = f"{self.data[name][other]:.2f}"
                max_width = max(max_width, len(value_str))
            col_widths[name] = max_width + 2
        
        # Build header
        result = "      "  # Space for row labels
        for name in self.names:
            result += f"{name:>{col_widths[name]}}"
        result += "\n"
        
        # Build rows
        for row_name in self.names:
            result += f"{row_name:<6}"
            for col_name in self.names:
                value = self.data[row_name][col_name]
                result += f"{value:>{col_widths[col_name]}.2f}"
            result += "\n"
        
        return result.rstrip()


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

    def tabulate(self) -> LedgerMatrix:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: A LedgerMatrix of who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        matrix = LedgerMatrix(names)

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    matrix.add_to_value(payer, payee, -value)
                    matrix.add_to_value(payee, payer, value)

        return matrix
