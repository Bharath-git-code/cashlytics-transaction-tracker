#!/usr/bin/env python3
"""
Test script to verify database functionality
"""

from database import DatabaseManager


def test_database():
    print("Testing database functionality...")

    # Initialize database
    db = DatabaseManager()
    print("✓ Database initialized")

    # Test creating a book
    book_id = db.create_book("Test Book")
    print(f"✓ Created book with ID: {book_id}")

    # Test getting books
    books = db.get_books()
    print(f"✓ Found {len(books)} books: {books}")

    # Test getting balance (should be 0 initially)
    balance = db.get_balance(book_id)
    print(f"✓ Initial balance: {balance}")

    # Test adding a transaction
    db.add_transaction(book_id, 100.0, "Test income", "Food", "Cash", True)
    print("✓ Added cash in transaction")

    # Test adding cash out transaction
    db.add_transaction(book_id, 50.0, "Test expense", "Transport", "Card", False)
    print("✓ Added cash out transaction")

    # Test getting new balance
    new_balance = db.get_balance(book_id)
    print(f"✓ New balance: {new_balance}")

    # Test getting transactions
    transactions = db.get_transactions(book_id)
    print(f"✓ Found {len(transactions)} transactions")

    # Test dropdown options
    types = db.get_dropdown_options("transaction_type")
    print(f"✓ Transaction types: {types}")

    payment_modes = db.get_dropdown_options("payment_mode")
    print(f"✓ Payment modes: {payment_modes}")

    print("\n🎉 All database tests passed!")


if __name__ == "__main__":
    test_database()
