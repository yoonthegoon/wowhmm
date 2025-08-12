# wowhmm

Who owes [whom](https://en.wiktionary.org/wiki/whom#Usage_notes) how much money?

![wowhmm](https://github.com/yoonthegoon/wowhmm/blob/main/media/wowhmm.png?raw=true)

## Installation

<!-- TODO: Set this up with PyPI. -->

```bash
pip install wowhmm
```

**No external dependencies required!** This package uses only Python's standard library.

## Usage

You first provide a list of who spent how much on whom.
In the example below, Alice spent $349.95 on a BnB for everyone.
To figure out the net amount owed to and from each person, call `tabulate` to return a nested dictionary.

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
{'Alice': {'Alice': 0.0, 'Bob': -42.77, 'Carol': -87.49, 'Dan': -69.37}, 'Bob': {'Alice': 42.77, 'Bob': 0.0, 'Carol': -10.51, 'Dan': -26.6}, 'Carol': {'Alice': 87.49, 'Bob': 10.51, 'Carol': 0.0, 'Dan': 3.63}, 'Dan': {'Alice': 69.37, 'Bob': 26.6, 'Carol': -3.63, 'Dan': 0.0}}
>>>
>>> print(ledger.tabulate_matrix())
       Alice    Bob  Carol    Dan
Alice   0.00 -42.77 -87.49 -69.37
Bob    42.77   0.00 -10.51 -26.60
Carol  87.49  10.51   0.00   3.63
Dan    69.37  26.60  -3.63   0.00
```

`tabulate()` returns a nested dictionary and rounds each value to the penny. Use `tabulate_matrix()` for a formatted table display.
With row headers being who and column headers being whom, the data is the amount who owes whom.
A value of 0 means no money is owed.
A negative value means that who is actually owed whom by that absolute value.
In the example above, Bob owes Alice $42.77.
