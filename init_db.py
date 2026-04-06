from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sneakervault.db"
DATA_DIR = BASE_DIR / "data"


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = OFF;

        DROP TABLE IF EXISTS Inventory;
        DROP TABLE IF EXISTS PurchasePrice;
        DROP TABLE IF EXISTS Customer;
        DROP TABLE IF EXISTS Supplier;
        DROP TABLE IF EXISTS Sneaker;

        CREATE TABLE Sneaker (
            ID INTEGER PRIMARY KEY,
            Brand TEXT NOT NULL,
            Model TEXT NOT NULL,
            Colorway TEXT NOT NULL,
            ReleaseDate TEXT,
            UNIQUE (Brand, Model, Colorway)
        );

        CREATE TABLE Supplier (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Type TEXT NOT NULL,
            ContactInfo TEXT NOT NULL UNIQUE
        );

        CREATE TABLE Customer (
            ID INTEGER PRIMARY KEY,
            Phone TEXT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE PurchasePrice (
            SneakerID INTEGER NOT NULL,
            Size REAL NOT NULL,
            "Condition" TEXT NOT NULL,
            PurchasePrice REAL NOT NULL,
            PRIMARY KEY (SneakerID, Size, "Condition"),
            FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

        CREATE TABLE Inventory (
            ID INTEGER PRIMARY KEY,
            SneakerID INTEGER NOT NULL,
            SupplierID INTEGER NOT NULL,
            Size REAL NOT NULL,
            "Condition" TEXT NOT NULL,
            Status TEXT NOT NULL CHECK (Status IN ('Available', 'Reserved', 'Sold')),
            CustomerID INTEGER NULL,
            FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
                ON DELETE RESTRICT
                ON UPDATE CASCADE,
            FOREIGN KEY (SupplierID) REFERENCES Supplier(ID)
                ON DELETE RESTRICT
                ON UPDATE CASCADE,
            FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
                ON DELETE SET NULL
                ON UPDATE CASCADE,
            FOREIGN KEY (SneakerID, Size, "Condition") REFERENCES PurchasePrice(SneakerID, Size, "Condition")
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );

        PRAGMA foreign_keys = ON;
        """
    )


def load_csv(conn: sqlite3.Connection, file_name: str, query: str, transform=None) -> None:
    file_path = DATA_DIR / file_name
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [transform(row) if transform else row for row in reader]
        conn.executemany(query, rows)


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    create_schema(conn)

    load_csv(
        conn,
        "sneaker.csv",
        """
        INSERT INTO Sneaker (ID, Brand, Model, Colorway, ReleaseDate)
        VALUES (:ID, :Brand, :Model, :Colorway, :ReleaseDate)
        """,
    )

    load_csv(
        conn,
        "supplier.csv",
        """
        INSERT INTO Supplier (ID, Name, Type, ContactInfo)
        VALUES (:ID, :Name, :Type, :ContactInfo)
        """,
    )

    load_csv(
        conn,
        "customer.csv",
        """
        INSERT INTO Customer (ID, Phone, FirstName, LastName, Email)
        VALUES (:ID, :Phone, :FirstName, :LastName, :Email)
        """,
    )

    load_csv(
        conn,
        "purchase_price.csv",
        """
        INSERT INTO PurchasePrice (SneakerID, Size, "Condition", PurchasePrice)
        VALUES (:SneakerID, :Size, :Condition, :PurchasePrice)
        """,
    )

    def inv_transform(row: dict[str, str]) -> dict[str, str | None]:
        row["CustomerID"] = row["CustomerID"] or None
        return row

    load_csv(
        conn,
        "inventory.csv",
        """
        INSERT INTO Inventory (ID, SneakerID, SupplierID, Size, "Condition", Status, CustomerID)
        VALUES (:ID, :SneakerID, :SupplierID, :Size, :Condition, :Status, :CustomerID)
        """,
        transform=inv_transform,
    )

    conn.commit()
    conn.close()
    print(f"SQLite database initialized: {DB_PATH}")


if __name__ == "__main__":
    main()
