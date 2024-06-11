from typing import List, NamedTuple

import pandas as pd


class Spent(NamedTuple):
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
    def __init__(self, transactions: List[Spent] = None):
        """
        A ledger of transactions.

        :param transactions: A list of transactions
        """

        self.transactions = transactions or []
        if not all(isinstance(transaction, Spent) for transaction in self.transactions):
            self.transactions = [
                Spent(who, amount, for_whom) for who, amount, for_whom in transactions
            ]

    def tabulate(self) -> pd.DataFrame:
        """
        Tabulate who owes whom how much.
        Values are negative if the person owes money and positive if the person is owed money.
        Values are rounded to two decimal places.

        :return: A DataFrame of who owes whom how much
        """

        names = set(
            name for transaction in self.transactions for name in transaction[2]
        )
        names.update(transaction[0] for transaction in self.transactions)
        names = sorted(names)

        df = pd.DataFrame(0.0, index=names, columns=names)

        for payer, amount, payees in self.transactions:
            for payee in payees:
                if payer != payee:
                    value = round(amount / len(payees), 2)
                    df.loc[payer, payee] -= value
                    df.loc[payee, payer] += value

        return df
