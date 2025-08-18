# wowhmm

Who owes [whom](https://en.wiktionary.org/wiki/whom#Usage_notes) how much money?

![wowhmm](https://github.com/yoonthegoon/wowhmm/blob/main/media/wowhmm.png?raw=true)

A Rust library and CLI tool for calculating shared expenses and debts between people.

## Installation

### As a Rust Library

Add this to your `Cargo.toml`:

```toml
[dependencies]
wowhmm = "0.1.5"
```

### CLI Tool

```bash
cargo install wowhmm
```

Or build from source:

```bash
git clone https://github.com/yoonthegoon/wowhmm.git
cd wowhmm
cargo build --release
```

## Development

This project uses standard Rust tooling:

```bash
# Clone the repository
git clone https://github.com/yoonthegoon/wowhmm.git
cd wowhmm

# Build the project
cargo build

# Run tests
cargo test

# Run examples
cargo run --example basic_usage

# Build and run the CLI
cargo run
```

## Usage

### Library Usage

```rust
use wowhmm::{Ledger, Spend};

let ledger = Ledger::new(vec![
    Spend::new("Alice", 349.95, vec!["Alice", "Bob", "Carol", "Dan"]), // BnB
    Spend::new("Bob", 68.42, vec!["Alice", "Dan"]),                    // Alcohol
    Spend::new("Bob", 42.02, vec!["Alice", "Bob", "Carol", "Dan"]),    // Groceries
    Spend::new("Dan", 72.48, vec!["Alice", "Bob", "Carol", "Dan"]),    // Transportation
    Spend::new("Carol", 28.98, vec!["Carol", "Dan"]),                  // Movies
]);

println!("{}", ledger.tabulate_formatted());
```

Output:
```
         Alice      Bob    Carol      Dan
     Alice   0.00   -42.77   -87.49   -69.37
       Bob  42.77     0.00   -10.51   -26.60
     Carol  87.49    10.51     0.00     3.63
       Dan  69.37    26.60    -3.63     0.00
```

### CLI Usage

The CLI tool reads JSON transactions from stdin:

```bash
echo '[["Alice", 100.0, ["Alice", "Bob"]], ["Bob", 50.0, ["Alice", "Bob"]]]' | wowhmm
```

The `tabulate` method rounds each value to the penny.
With row headers being who and column headers being whom, the data is the amount who owes whom.
A value of 0 means no money is owed.
A negative value means that who is actually owed money by whom by that absolute value.
In the example above, Bob owes Alice $42.77.
