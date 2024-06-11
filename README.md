# wowhmm

Who owes [whom](https://en.wiktionary.org/wiki/whom#Usage_notes) how much money?

![wowhmm](https://github.com/yoonthegoon/wowhmm/blob/main/media/wowhmm.png?raw=true)

## Installation

<!-- TODO: Set this up with PyPI. -->

```bash
pip install wowhmm
```

## Usage

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
