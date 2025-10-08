# 📊 Bookkeeping System

A modern, web-based double-entry bookkeeping system built with Django. This application provides a complete solution for managing accounts, recording transactions, and generating financial reports.

## ✨ Features

- **Double-Entry Bookkeeping**: Proper debit/credit validation ensuring balanced transactions
- **Account Management**: Support for Assets, Liabilities, Equity, Income, and Expense accounts
- **Transaction Recording**: Create and manage journal entries with multiple accounts
- **Trial Balance**: Generate comprehensive trial balance reports
- **Export Functionality**: Export data to Excel (.xlsx) and PDF formats
- **Modern UI**: Responsive design with professional styling and interactive features
- **Real-time Validation**: Live balance checking during transaction entry

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- uv package manager

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the development server**:
   ```bash
   cd web
   uv run python manage.py runserver
   ```

   Or use the convenience script:
   ```bash
   python run_server.py
   ```

4. **Access the application**:
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Create accounts via the Django admin at `http://127.0.0.1:8000/admin/`

## 📋 Usage Guide

### 1. Setting Up Accounts

First, create your chart of accounts through the Django admin interface:

1. Go to `http://127.0.0.1:8000/admin/`
2. Navigate to "Bookkeeping" → "Accounts"
3. Add accounts for each category:
   - **Assets**: Cash, Bank, Inventory, Equipment, etc.
   - **Liabilities**: Accounts Payable, Loans, etc.
   - **Equity**: Owner's Equity, Retained Earnings, etc.
   - **Income**: Sales Revenue, Service Revenue, etc.
   - **Expenses**: Rent, Utilities, Salaries, etc.

### 2. Recording Transactions

1. Navigate to "New Transaction" from the main menu
2. Enter a description for the transaction
3. Add journal entries:
   - Select an account
   - Enter either a debit or credit amount (not both)
   - Add multiple entries as needed
4. The system will validate that total debits equal total credits
5. Save the transaction

### 3. Viewing Reports

- **Accounts List**: View all accounts with current balances
- **Transaction History**: See all recorded transactions
- **Trial Balance**: Generate comprehensive financial reports
- **Export Options**: Download reports in Excel or PDF format

## 🏗️ Technical Details

### Architecture

- **Backend**: Django 5.2+ with SQLite database
- **Frontend**: Modern HTML5/CSS3 with JavaScript
- **Styling**: Custom CSS with gradient backgrounds and glassmorphism effects
- **Export**: openpyxl for Excel, xhtml2pdf for PDF generation

### Key Components

- **Models**: Account, Transaction, LedgerEntry
- **Views**: Account management, transaction recording, reporting
- **Templates**: Responsive HTML templates with modern styling
- **Forms**: Dynamic form handling with validation
- **Admin**: Django admin interface for data management

### Database Schema

- **Account**: Stores account information and balances
- **Transaction**: Records transaction metadata
- **LedgerEntry**: Individual debit/credit entries linked to transactions

## 🔧 Development

### Running Tests

```bash
cd web
uv run python manage.py test
```

### Database Migrations

```bash
cd web
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Creating Superuser

```bash
cd web
uv run python manage.py createsuperuser
```

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds with glassmorphism effects
- **Interactive Elements**: Hover effects and smooth animations
- **Color Coding**: Visual indicators for different account types and balances
- **Real-time Validation**: Live feedback during data entry
- **Professional Styling**: Clean, business-appropriate interface

## 📊 Export Features

- **Excel Export**: Download ledger data as .xlsx files
- **PDF Export**: Generate trial balance reports as PDF documents
- **Formatted Reports**: Professional formatting for business use

## 🛠️ Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure to use `uv run` prefix for all commands
2. **Database errors**: Run migrations with `uv run python manage.py migrate`
3. **Permission errors**: Ensure proper file permissions in the project directory

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `uv sync`
2. Verify Django is working: `uv run python manage.py check`
3. Check the terminal output for specific error messages

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Bookkeeping! 📊✨**
