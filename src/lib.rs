//! # wowhmm
//!
//! Who owes whom how much money?
//!
//! This library helps you calculate the net amount owed between people
//! when splitting shared expenses.
//!
//! ## Example
//!
//! ```rust
//! use wowhmm::{Ledger, Spend};
//!
//! let ledger = Ledger::new(vec![
//!     Spend::new("Alice", 349.95, vec!["Alice", "Bob", "Carol", "Dan"]), // BnB
//!     Spend::new("Bob", 68.42, vec!["Alice", "Dan"]),                    // Alcohol
//!     Spend::new("Bob", 42.02, vec!["Alice", "Bob", "Carol", "Dan"]),    // Groceries
//!     Spend::new("Dan", 72.48, vec!["Alice", "Bob", "Carol", "Dan"]),    // Transportation
//!     Spend::new("Carol", 28.98, vec!["Carol", "Dan"]),                  // Movies
//! ]);
//!
//! let table = ledger.tabulate();
//! println!("{:#?}", table);
//! ```

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Represents a single spending transaction
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Spend {
    /// The person who spent the money
    pub who: String,
    /// The amount of money spent
    pub amount: f64,
    /// The people for whom the money was spent
    pub for_whom: Vec<String>,
}

impl Spend {
    /// Create a new Spend transaction
    ///
    /// # Arguments
    /// * `who` - The person who spent the money
    /// * `amount` - The amount of money spent
    /// * `for_whom` - The people for whom the money was spent
    ///
    /// # Example
    /// ```rust
    /// use wowhmm::Spend;
    ///
    /// let spend = Spend::new("Alice", 100.0, vec!["Alice", "Bob"]);
    /// ```
    pub fn new<S: Into<String>>(who: S, amount: f64, for_whom: Vec<S>) -> Self {
        Self {
            who: who.into(),
            amount,
            for_whom: for_whom.into_iter().map(|s| s.into()).collect(),
        }
    }
}

/// A ledger of spending transactions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Ledger {
    /// List of spending transactions
    pub transactions: Vec<Spend>,
}

impl Ledger {
    /// Create a new ledger with the given transactions
    ///
    /// # Arguments
    /// * `transactions` - A list of spending transactions
    ///
    /// # Example
    /// ```rust
    /// use wowhmm::{Ledger, Spend};
    ///
    /// let ledger = Ledger::new(vec![
    ///     Spend::new("Alice", 100.0, vec!["Alice", "Bob"]),
    /// ]);
    /// ```
    pub fn new(transactions: Vec<Spend>) -> Self {
        Self { transactions }
    }

    /// Create an empty ledger
    pub fn empty() -> Self {
        Self {
            transactions: Vec::new(),
        }
    }

    /// Add a transaction to the ledger
    ///
    /// # Arguments
    /// * `transaction` - The transaction to add
    pub fn add_transaction(&mut self, transaction: Spend) {
        self.transactions.push(transaction);
    }

    /// Get all unique names from the ledger
    fn get_all_names(&self) -> Vec<String> {
        let mut names = std::collections::HashSet::new();
        
        for transaction in &self.transactions {
            names.insert(transaction.who.clone());
            for person in &transaction.for_whom {
                names.insert(person.clone());
            }
        }
        
        let mut sorted_names: Vec<String> = names.into_iter().collect();
        sorted_names.sort();
        sorted_names
    }

    /// Tabulate who owes whom how much
    ///
    /// Returns a HashMap where the outer key is the person who owes money,
    /// the inner key is the person who is owed money, and the value is the amount.
    /// 
    /// Values are negative if the person owes money and positive if the person is owed money.
    /// Values are rounded to two decimal places (cents).
    ///
    /// # Returns
    /// A HashMap representing the debt matrix
    ///
    /// # Example
    /// ```rust
    /// use wowhmm::{Ledger, Spend};
    ///
    /// let ledger = Ledger::new(vec![
    ///     Spend::new("Alice", 100.0, vec!["Alice", "Bob"]),
    /// ]);
    /// let table = ledger.tabulate();
    /// ```
    pub fn tabulate(&self) -> HashMap<String, HashMap<String, f64>> {
        let names = self.get_all_names();
        let mut result = HashMap::new();

        // Initialize the matrix with zeros
        for name1 in &names {
            let mut inner_map = HashMap::new();
            for name2 in &names {
                inner_map.insert(name2.clone(), 0.0);
            }
            result.insert(name1.clone(), inner_map);
        }

        // Process each transaction
        for transaction in &self.transactions {
            let payer = &transaction.who;
            let amount = transaction.amount;
            let payees = &transaction.for_whom;
            
            for payee in payees {
                if payer != payee {
                    let value = (amount / payees.len() as f64 * 100.0).round() / 100.0;
                    
                    // Payer is owed money (negative debt to payee)
                    if let Some(payer_map) = result.get_mut(payer) {
                        if let Some(current_value) = payer_map.get_mut(payee) {
                            *current_value -= value;
                        }
                    }
                    
                    // Payee owes money (positive debt to payer)
                    if let Some(payee_map) = result.get_mut(payee) {
                        if let Some(current_value) = payee_map.get_mut(payer) {
                            *current_value += value;
                        }
                    }
                }
            }
        }

        // Round all values to 2 decimal places
        for inner_map in result.values_mut() {
            for value in inner_map.values_mut() {
                *value = (*value * 100.0).round() / 100.0;
            }
        }

        result
    }

    /// Get a formatted string representation of the debt table
    ///
    /// # Returns
    /// A string showing the debt matrix in a readable format
    pub fn tabulate_formatted(&self) -> String {
        let table = self.tabulate();
        let names = self.get_all_names();
        
        if names.is_empty() {
            return "No transactions recorded.".to_string();
        }

        let mut result = String::new();
        
        // Header row
        result.push_str(&format!("{:>10}", ""));
        for name in &names {
            result.push_str(&format!("{:>10}", name));
        }
        result.push('\n');
        
        // Data rows
        for row_name in &names {
            result.push_str(&format!("{:>10}", row_name));
            if let Some(row) = table.get(row_name) {
                for col_name in &names {
                    if let Some(value) = row.get(col_name) {
                        result.push_str(&format!("{:>10.2}", value));
                    } else {
                        result.push_str(&format!("{:>10}", "0.00"));
                    }
                }
            }
            result.push('\n');
        }
        
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_ledger() {
        let ledger = Ledger::empty();
        let table = ledger.tabulate();
        assert!(table.is_empty());
    }

    #[test]
    fn test_single_transaction() {
        let ledger = Ledger::new(vec![
            Spend::new("Alice", 100.0, vec!["Alice", "Bob"]),
        ]);
        let table = ledger.tabulate();
        
        // Alice should be owed $50 by Bob
        assert_eq!(table["Alice"]["Bob"], -50.0);
        assert_eq!(table["Bob"]["Alice"], 50.0);
        assert_eq!(table["Alice"]["Alice"], 0.0);
        assert_eq!(table["Bob"]["Bob"], 0.0);
    }

    #[test]
    fn test_example_from_readme() {
        let ledger = Ledger::new(vec![
            Spend::new("Alice", 349.95, vec!["Alice", "Bob", "Carol", "Dan"]), // BnB
            Spend::new("Bob", 68.42, vec!["Alice", "Dan"]),                    // Alcohol
            Spend::new("Bob", 42.02, vec!["Alice", "Bob", "Carol", "Dan"]),    // Groceries
            Spend::new("Dan", 72.48, vec!["Alice", "Bob", "Carol", "Dan"]),    // Transportation
            Spend::new("Carol", 28.98, vec!["Carol", "Dan"]),                  // Movies
        ]);

        let table = ledger.tabulate();
        
        // Check some key values from the expected output
        assert_eq!(table["Alice"]["Alice"], 0.0);
        assert_eq!(table["Bob"]["Alice"], 42.77);
        assert_eq!(table["Alice"]["Bob"], -42.77);
    }

    #[test]
    fn test_spend_creation() {
        let spend = Spend::new("Alice", 100.0, vec!["Alice", "Bob"]);
        assert_eq!(spend.who, "Alice");
        assert_eq!(spend.amount, 100.0);
        assert_eq!(spend.for_whom, vec!["Alice", "Bob"]);
    }

    #[test]
    fn test_formatted_output() {
        let ledger = Ledger::new(vec![
            Spend::new("Alice", 100.0, vec!["Alice", "Bob"]),
        ]);
        let formatted = ledger.tabulate_formatted();
        assert!(formatted.contains("Alice"));
        assert!(formatted.contains("Bob"));
        assert!(formatted.contains("50.00"));
    }
}