# wowhmm

Who owes [whom](https://en.wiktionary.org/wiki/whom#Usage_notes) how much money?

![wowhmm](https://github.com/yoonthegoon/wowhmm/blob/main/media/wowhmm.png?raw=true)

## Installation

<!-- TODO: Set this up with PyPI. -->

```bash
pip install wowhmm
```

## Usage

You first provide a list of who spent how much on whom.
In the example below, Alice spent $349.95 on a BnB for everyone.
To figure out the net amount owed to and from each person, call `tabulate` to return a `pandas.DataFrame`.

```python
>>> from wowhmm import Ledger
>>>
>>> ledger = Ledger(
...     [
...         ("Alice", 349.95, ["Alice", "Bob", "Carol", "Dan"]),  # BnB
...         ("Bob", 68.42, ["Alice", "Dan"]),  # Alcohol
...         ("Bob", 42.02, ["Alice", "Bob", "Carol", "Dan"]),  # Groceries
...         ("Dan", 72.48, ["Alice", "Bob", "Carol", "Dan"]),  # Transportation
...         ("Carol", 28.98, ["Carol", "Dan"]),  # Movies
...     ]
... )
>>>
>>> ledger.tabulate()
       Alice    Bob  Carol    Dan
Alice   0.00 -42.77 -87.49 -69.37
Bob    42.77   0.00 -10.51 -26.60
Carol  87.49  10.51   0.00   3.63
Dan    69.37  26.60  -3.63   0.00
```

`tabulate` rounds each value to the penny.
With row headers being who and column headers being whom, the data is the amount who owes whom.
A value of 0 means no money is owed.
A negative value means that who is actually owed whom by that absolute value.
In the example above, Bob owes Alice $42.77.
