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

        :return: A dictionary of dictionaries representing who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        # Create nested dictionary structure similar to DataFrame
        result = {name: {other_name: 0.0 for other_name in names} for name in names}

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    result[payer][payee] -= value
                    result[payee][payer] += value

        return result
