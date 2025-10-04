import sqlite3
import json
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="transaction_tracker.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create books table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_date TEXT NOT NULL
            )
        """
        )

        # Create transactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                payment_mode TEXT NOT NULL,
                transaction_date TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        """
        )

        # Create settings table for dropdown options
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_type TEXT NOT NULL,
                value TEXT NOT NULL
            )
        """
        )

        # Insert default dropdown options only if settings table is empty
        cursor.execute("SELECT COUNT(*) FROM settings")
        settings_count = cursor.fetchone()[0]

        if settings_count == 0:
            # Only add defaults if no settings exist
            default_types = [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Other",
            ]
            default_payment_modes = [
                "Cash",
                "Credit Card",
                "Debit Card",
                "UPI",
                "Net Banking",
                "Cheque",
            ]

            for type_val in default_types:
                cursor.execute(
                    """
                    INSERT INTO settings (setting_type, value) VALUES (?, ?)
                """,
                    ("transaction_type", type_val),
                )

            for mode_val in default_payment_modes:
                cursor.execute(
                    """
                    INSERT INTO settings (setting_type, value) VALUES (?, ?)
                """,
                    ("payment_mode", mode_val),
                )

        conn.commit()
        conn.close()

    def create_book(self, name):
        """Create a new transaction book"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO books (name, created_date) VALUES (?, ?)
            """,
                (name, datetime.now().isoformat()),
            )
            conn.commit()
            book_id = cursor.lastrowid
            conn.close()
            return book_id
        except sqlite3.IntegrityError:
            return None  # Book name already exists

    def get_books(self):
        """Get all books"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, created_date FROM books ORDER BY created_date DESC"
        )
        books = cursor.fetchall()
        conn.close()
        return books

    def delete_book(self, book_id):
        """Delete a book and all its transactions"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE book_id = ?", (book_id,))
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

    def add_transaction(
        self, book_id, amount, description, transaction_type, payment_mode, is_cash_in
    ):
        """Add a new transaction"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Make amount negative for cash out
        final_amount = amount if is_cash_in else -amount

        cursor.execute(
            """
            INSERT INTO transactions (book_id, amount, description, transaction_type, payment_mode, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                book_id,
                final_amount,
                description,
                transaction_type,
                payment_mode,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def get_transactions(self, book_id):
        """Get all transactions for a book"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, description, transaction_type, payment_mode, transaction_date
            FROM transactions WHERE book_id = ? ORDER BY transaction_date DESC
        """,
            (book_id,),
        )
        transactions = cursor.fetchall()
        conn.close()
        return transactions

    def get_balance(self, book_id):
        """Get the balance for a book"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE book_id = ?", (book_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] is not None else 0.0

    def get_dropdown_options(self, setting_type):
        """Get dropdown options for transaction types or payment modes"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM settings WHERE setting_type = ?", (setting_type,)
        )
        options = [row[0] for row in cursor.fetchall()]
        conn.close()
        return options

    def add_dropdown_option(self, setting_type, value):
        """Add a new dropdown option"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO settings (setting_type, value) VALUES (?, ?)
            """,
                (setting_type, value),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_dropdown_option(self, setting_type, value):
        """Remove a dropdown option"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM settings WHERE setting_type = ? AND value = ?
        """,
            (setting_type, value),
        )
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def update_transaction(
        self,
        trans_id,
        amount,
        description,
        transaction_type,
        payment_mode,
        is_cash_in,
        transaction_date=None,
    ):
        """Update an existing transaction"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Make amount negative for cash out
        final_amount = amount if is_cash_in else -amount

        # Use provided date or current datetime
        if transaction_date is None:
            transaction_date = datetime.now().isoformat()

        cursor.execute(
            """
            UPDATE transactions 
            SET amount = ?, description = ?, transaction_type = ?, payment_mode = ?, transaction_date = ?
            WHERE id = ?
        """,
            (
                final_amount,
                description,
                transaction_type,
                payment_mode,
                transaction_date,
                trans_id,
            ),
        )

        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def get_transaction_by_id(self, trans_id):
        """Get a specific transaction by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, description, transaction_type, payment_mode, transaction_date
            FROM transactions WHERE id = ?
        """,
            (trans_id,),
        )
        transaction = cursor.fetchone()
        conn.close()
        return transaction
