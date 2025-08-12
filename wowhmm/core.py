from typing import List, NamedTuple, Dict


class Table:
    """
    A simple table implementation to replace pandas DataFrame functionality.
    """
    
    def __init__(self, data: Dict[str, Dict[str, float]], index: List[str], columns: List[str]):
        self.data = data
        self.index = index
        self.columns = columns
    
    def loc(self, row: str, col: str) -> float:
        """Get value at specific row and column."""
        return self.data[row][col]
    
    def set_loc(self, row: str, col: str, value: float):
        """Set value at specific row and column."""
        self.data[row][col] = value
    
    def __str__(self) -> str:
        """String representation of the table."""
        # Calculate column widths for formatting
        col_widths = {}
        for col in self.columns:
            col_widths[col] = max(len(col), max(len(f"{self.data[row][col]:.2f}") for row in self.index))
        
        # Add width for row names
        row_name_width = max(len(row) for row in self.index)
        
        # Build the table string
        lines = []
        
        # Header row
        header = " " * row_name_width + " "
        for col in self.columns:
            header += f"{col:>{col_widths[col]}} "
        lines.append(header.rstrip())
        
        # Data rows
        for row in self.index:
            line = f"{row:<{row_name_width}} "
            for col in self.columns:
                value = self.data[row][col]
                line += f"{value:>{col_widths[col]}.2f} "
            lines.append(line.rstrip())
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
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

    def tabulate(self) -> Table:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: A Table of who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        # Initialize the data structure
        data = {}
        for name in names:
            data[name] = {}
            for other_name in names:
                data[name][other_name] = 0.0

        # Create the table
        table = Table(data, names, names)

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    table.set_loc(payer, payee, table.loc(payer, payee) - value)
                    table.set_loc(payee, payer, table.loc(payee, payer) + value)

        return table
