use wowhmm::{Ledger, Spend};

fn main() {
    // Example from the README
    let ledger = Ledger::new(vec![
        Spend::new("Alice", 349.95, vec!["Alice", "Bob", "Carol", "Dan"]), // BnB
        Spend::new("Bob", 68.42, vec!["Alice", "Dan"]),                    // Alcohol
        Spend::new("Bob", 42.02, vec!["Alice", "Bob", "Carol", "Dan"]),    // Groceries
        Spend::new("Dan", 72.48, vec!["Alice", "Bob", "Carol", "Dan"]),    // Transportation
        Spend::new("Carol", 28.98, vec!["Carol", "Dan"]),                  // Movies
    ]);

    println!("Debt calculation:");
    println!("{}", ledger.tabulate_formatted());
    
    println!("\nExplanation:");
    println!("- Row headers are 'who' and column headers are 'whom'");
    println!("- Values show the amount 'who' owes 'whom'");
    println!("- Negative values mean 'who' is actually owed money by 'whom'");
    println!("- For example: Bob owes Alice $42.77");
}