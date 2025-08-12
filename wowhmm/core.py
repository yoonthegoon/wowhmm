from typing import List, NamedTuple, Dict


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

    def tabulate(self) -> Dict[str, Dict[str, float]]:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: A dictionary of who owes whom how much (nested dict format)
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        # Initialize nested dictionary with 0.0 values
        result = {name: {other: 0.0 for other in names} for name in names}

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    result[payer][payee] -= value
                    result[payee][payer] += value

        return result

    def tabulate_matrix(self) -> str:
        """
        Return a formatted string representation of the tabulation matrix.
        Similar to pandas DataFrame string representation.

        :return: A formatted string showing who owes whom how much
        """
        data = self.tabulate()
        if not data:
            return "No transactions"

        names = list(data.keys())
        
        # Calculate column widths
        max_name_width = max(len(name) for name in names)
        max_value_width = max(
            len(f"{value:.2f}") 
            for row in data.values() 
            for value in row.values()
        )
        col_width = max(max_name_width, max_value_width, 6)

        # Build the header
        header = " " * max_name_width + "  " + "  ".join(f"{name:>{col_width}}" for name in names)
        
        # Build the rows
        rows = []
        for row_name in names:
            row_values = "  ".join(f"{data[row_name][col_name]:>{col_width}.2f}" for col_name in names)
            rows.append(f"{row_name:<{max_name_width}}  {row_values}")

        return header + "\n" + "\n".join(rows)
