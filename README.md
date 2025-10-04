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

This project includes automated GitHub Actions workflows for building Android APKs:

### 🚀 Quick Build (Recommended)

1. **Push changes to GitHub**
2. **Go to Actions tab** in your repository
3. **Run "Build APK (Minimal Working)"** workflow
4. **Download APK** from artifacts

### Available Workflows

- **build-apk-minimal.yml**: Fast, essential-only build
- **build-apk-complete.yml**: Comprehensive build with all tools
- **build-apk-recommended.yml**: Balanced approach (recommended)

### Manual Build (Local)

If you want to build locally:

```bash
# Install buildozer
pip install buildozer cython

# Build debug APK
buildozer android debug
```

**Note**: Local builds require Android SDK setup and can be complex. GitHub Actions is recommended for hassle-free APK generation.

### Build Status

✅ **App Development**: Complete  
✅ **Build Environment**: Ready  
✅ **License Handling**: Automated  
🔄 **APK Generation**: In Progress  

See `BUILD_APK.md` for detailed build documentation and troubleshooting.

## Contributing

Feel free to fork this project and submit pull requests for improvements.

## License

This project is open source and available under the MIT License.
