# Transaction Tracker

A cross-platform mobile transaction tracker app built with Kivy and KivyMD.

## Features

- **Multiple Books**: Create and manage different transaction books (e.g., Personal, Business, Travel)
- **Transaction Management**: Add Cash In and Cash Out transactions
- **Detailed Transactions**: Each transaction includes amount, description, type, and payment mode
- **Balance Tracking**: Real-time balance calculation and display
- **Transaction History**: View all transactions with detailed information
- **Customizable Categories**: Add/remove transaction types and payment modes in settings
- **Material Design UI**: Beautiful, modern interface using KivyMD

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app:

```bash
python main.py
```

### Basic Workflow

1. **Create a Book**: Start by creating your first transaction book
2. **Add Transactions**: Click "Cash In" or "Cash Out" to add transactions
3. **Fill Details**: Enter amount, description, select type and payment mode
4. **View History**: See all transactions and current balance
5. **Customize**: Use Settings to add your own transaction types and payment modes

## Project Structure

```
transaction_tracker/
├── main.py                 # Main application entry point
├── database.py             # SQLite database management
├── requirements.txt        # Python dependencies
├── screens/               # UI screens
│   ├── __init__.py
│   ├── book_list.py       # Books management screen
│   ├── transaction_list.py # Transaction list and balance
│   ├── transaction_form.py # Add new transaction
│   └── settings.py        # App settings and customization
└── README.md              # This file
```

## Database Schema

The app uses SQLite with three main tables:

- **books**: Stores transaction books
- **transactions**: Stores all transactions linked to books
- **settings**: Stores customizable dropdown options

## Building for Android

To build for Android, you can use:

1. **Buildozer** (recommended):

   ```bash
   pip install buildozer
   buildozer android debug
   ```

2. **Python-for-Android (p4a)**:
   ```bash
   pip install python-for-android
   p4a apk --private . --package=com.example.transactiontracker --name="Transaction Tracker" --version=0.1 --bootstrap=sdl2 --requirements=python3,kivy,kivymd
   ```

## Contributing

Feel free to fork this project and submit pull requests for improvements.

## License

This project is open source and available under the MIT License.
