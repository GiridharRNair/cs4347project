# SneakerVault

A database-driven sneaker reselling management system.

## Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

```bash
python app.py
```

The server starts at `http://localhost:5000`

- Database initializes automatically on first run
- CSV data loads from the `data/` directory
- All HTML forms and pages are fully functional

## Features

- **Add Sneaker Models** - Create new product types
- **Manage Inventory** - Track individual stock items
- **Record Sales** - Mark items as sold and link to customers
- **Customer Management** - Add and search customers
- **Supplier Management** - Manage suppliers
- **Inventory Search** - Filter by brand, size, and status
- **Reports** - View inventory breakdown, sales by model, supplier activity

All IDs auto-generate if left blank in forms.
