use serde_json;
use std::io::{self, Read};
use wowhmm::{Ledger, Spend};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("wowhmm - Who owes whom how much money?");
    println!("========================================");
    
    // Read JSON from stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    
    // Parse JSON input
    let transactions: Vec<(String, f64, Vec<String>)> = serde_json::from_str(&input)?;
    
    // Convert to Spend objects
    let spends: Vec<Spend> = transactions
        .into_iter()
        .map(|(who, amount, for_whom)| Spend::new(who, amount, for_whom))
        .collect();
    
    // Create ledger and calculate
    let ledger = Ledger::new(spends);
    println!("{}", ledger.tabulate_formatted());
    
    Ok(())
}

fn show_usage() {
    println!("Usage:");
    println!("  echo '[transactions]' | wowhmm");
    println!();
    println!("Transaction format (JSON):");
    println!("  [[\"who\", amount, [\"for_whom1\", \"for_whom2\"]], ...]");
    println!();
    println!("Example:");
    println!("  echo '[[\"Alice\", 100.0, [\"Alice\", \"Bob\"]], [\"Bob\", 50.0, [\"Alice\", \"Bob\"]]]' | wowhmm");
}