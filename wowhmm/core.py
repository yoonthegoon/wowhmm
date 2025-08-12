from typing import List, NamedTuple, Dict


class OwingTable:
    """
    A table-like structure to track who owes whom how much money.
    Replacement for pandas DataFrame for this specific use case.
    """
    
    def __init__(self, data: Dict[str, Dict[str, float]], index: List[str], columns: List[str]):
        self.data = data
        self.index = index
        self.columns = columns
    
    def __str__(self) -> str:
        """String representation of the owing table."""
        # Calculate column widths
        header_width = max(len(name) for name in self.index)
        
        # Build the header row
        result = [' ' * header_width]
        for col in self.columns:
            result.append(f"{col:>8}")
        header = '  '.join(result) + '\n'
        
        # Build data rows
        rows = []
        for row_name in self.index:
            row = [f"{row_name:<{header_width}}"]
            for col_name in self.columns:
                value = self.data[row_name][col_name]
                row.append(f"{value:8.2f}")
            rows.append('  '.join(row))
        
        return header + '\n'.join(rows)
    
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

    def tabulate(self) -> OwingTable:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: An OwingTable of who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        # Initialize data structure
        data = {name: {other_name: 0.0 for other_name in names} for name in names}

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    data[payer][payee] -= value
                    data[payee][payer] += value

        return OwingTable(data, names, names)
